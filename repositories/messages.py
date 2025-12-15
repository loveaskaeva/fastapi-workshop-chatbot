from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Message


async def create_pair(db: AsyncSession, session_id: int, user_text: str, bot_text: str) -> Message:
    user_msg = Message(session_id=session_id, sender="user", text=user_text)
    bot_msg = Message(session_id=session_id, sender="bot", text=bot_text)
    db.add_all([user_msg, bot_msg])
    await db.commit()
    await db.refresh(bot_msg)
    return bot_msg


async def list_by_session(db: AsyncSession, session_id: int) -> list[Message]:
    res = await db.execute(select(Message).where(Message.session_id == session_id).order_by(Message.sent_at.asc()))
    return list(res.scalars().all())
