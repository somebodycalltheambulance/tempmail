import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.messages.models import Message


async def get_messages(session: AsyncSession, mailbox_id: uuid.UUID) -> list[Message]:
    """Достать все письма из ящика, новые сверху"""
    result = await session.execute(
        select(Message)
        .where(Message.mailbox_id == mailbox_id)
        .order_by(Message.received_at.desc())
    )
    return list(result.scalars().all())


async def get_message(session: AsyncSession, mailbox_id: uuid.UUID, message_id:uuid.UUID) -> Message | None:
    """Прочитать письмо"""
    result = await session.execute(
        select(Message)
        .where(Message.mailbox_id == mailbox_id, Message.id == message_id)
    )
    return result.scalar_one_or_none()