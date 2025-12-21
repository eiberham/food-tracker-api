from app.database import get_cache

class RedisService:
    client = get_cache()

    @classmethod
    async def set(cls, key: str, value: str, expire: int = None):
        await cls.client.set(key, value, expire)

    @classmethod
    async def get(cls, key: str):
        return await cls.client.get(key)

    @classmethod
    async def expire(cls, key: str, seconds: int):
        await cls.client.expire(key, seconds)