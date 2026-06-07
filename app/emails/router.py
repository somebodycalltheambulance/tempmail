from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.emails import service
from app.emails.schemas import MailboxResponse


# Роутер для эндпойнтов, связанных с ящиками
router = APIRouter(prefix="/mailboxes", tags=["mailboxes"])


@router.post(
    "", # путь относительно prefix - POST /mailboxes
    response_model=MailboxResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_mailbox(
    db: AsyncSession = Depends(get_db),
) -> MailboxResponse:
    # 1. Зову сервис - он создает ящик, возвращает (обьект, токен)
    mailbox, raw_token = await service.create_mailbox(db)
    
    # 2. Собираю ответ ВРУЧНУЮ - токен подставляется из памяти
    return MailboxResponse(
        id=mailbox.id,
        address=mailbox.address,
        token=raw_token,
        expires_at=mailbox.expires_at,
        is_extended=mailbox.is_extended,
    )
    
    