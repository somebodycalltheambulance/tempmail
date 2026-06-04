from redis.asyncio import Redis

from app.config import settings


#Клиент Redis - один на приложение, внутри пул соединений.
#Создается при импорте, переиспользуется везде
redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
)

async def get_redis() -> Redis:
    return redis_client