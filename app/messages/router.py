from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.messages import service
from app.emails.models import Mailbox
from app.emails.dependencies import get_authorized_mailbox
from app.messages.schemas import MessageListResponse, MessagePreview

router = APIRouter(prefix="/mailboxes/{mailbox_id}/messages", tags=["messages"])


@router.get("", response_model=MessageListResponse)
async def list_messages(
    mailbox: Mailbox = Depends(get_authorized_mailbox),
    db: AsyncSession = Depends(get_db),
) -> MessageListResponse:
    messages = await service.get_messages(db, mailbox.id)
    
    return MessageListResponse(
        messages=[MessagePreview.model_validate(m) for m in messages],
        count=len(messages),
    )