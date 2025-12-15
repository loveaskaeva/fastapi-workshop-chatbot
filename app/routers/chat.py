from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Session, Message, User
from app.schemas import CreateSessionResponse, MessageRequest, MessageResponse, HistoryResponse
from app.auth import get_current_user
from app.bot_logic import reply


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/session", response_model=CreateSessionResponse)
async def create_session(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = Session(user_id=current_user.id)
    db.add(s)
    await db.commit()
    await db.refresh(s)
    return CreateSessionResponse(session_id=s.id)


@router.post("/message", response_model=MessageResponse)
async def post_message(payload: MessageRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.scalar(select(Session).where(Session.id == payload.session_id))
    if not s or s.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_msg = Message(session_id=s.id, sender="user", text=payload.text)
    bot_text = reply(payload.text)
    bot_msg = Message(session_id=s.id, sender="bot", text=bot_text)
    db.add_all([user_msg, bot_msg])
    await db.commit()
    await db.refresh(bot_msg)
    return MessageResponse(sender=bot_msg.sender, text=bot_msg.text, sent_at=bot_msg.sent_at)


@router.get("/history/{session_id}", response_model=HistoryResponse)
async def history(session_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    s = await db.scalar(select(Session).where(Session.id == session_id))
    if not s or s.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    msgs = (await db.execute(select(Message).where(Message.session_id == session_id).order_by(Message.sent_at.asc()))).scalars().all()
    return HistoryResponse(
        session_id=session_id,
        messages=[MessageResponse(sender=m.sender, text=m.text, sent_at=m.sent_at) for m in msgs],
    )
