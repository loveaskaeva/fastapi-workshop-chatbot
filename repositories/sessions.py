from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Session


async def create_session(db: AsyncSession, user_id: int) -> Session:
    s = Session(user_id=user_id)
    db.add(s)
    await db.commit()
    await db.refresh(s)
    return s


async def get_session(db: AsyncSession, session_id: int) -> Session | None:
    return await db.scalar(select(Session).where(Session.id == session_id))
