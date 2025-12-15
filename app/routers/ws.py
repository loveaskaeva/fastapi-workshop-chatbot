from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.database import AsyncSessionLocal
from app.models import User, Session, Message
from app.bot_logic import reply


router = APIRouter(prefix="/ws", tags=["ws"])


@router.websocket("/chat")
async def chat_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    session_id = websocket.query_params.get("session_id")
    await websocket.accept()
    if not token or not session_id:
        await websocket.close(code=4401)
        return
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
    except Exception:
        await websocket.close(code=4401)
        return
    async with AsyncSessionLocal() as db:
        user = await db.scalar(select(User).where(User.username == username))
        if not user:
            await websocket.close(code=4401)
            return
        s = await db.scalar(select(Session).where(Session.id == int(session_id)))
        if not s or s.user_id != user.id:
            await websocket.close(code=4404)
            return
        try:
            while True:
                data = await websocket.receive_json()
                text = data.get("text") or ""
                if not text.strip():
                    await websocket.send_json({"error": "empty"})
                    continue
                user_msg = Message(session_id=s.id, sender="user", text=text)
                bot_text = reply(text)
                bot_msg = Message(session_id=s.id, sender="bot", text=bot_text)
                db.add_all([user_msg, bot_msg])
                await db.commit()
                await db.refresh(bot_msg)
                await websocket.send_json({"sender": "bot", "text": bot_text, "sent_at": bot_msg.sent_at.isoformat()})
        except WebSocketDisconnect:
            return
