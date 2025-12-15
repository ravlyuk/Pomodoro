from redis import asyncio as redis

from settings import Settings


def get_redis_connection(host="localhost", port=6379, db=0) -> redis.Redis:
    settings = Settings()  # type: ignore
    client = redis.Redis(
        host=settings.CACHE_HOST, port=settings.CACHE_PORT, db=settings.CACHE_DB
    )
    return client
