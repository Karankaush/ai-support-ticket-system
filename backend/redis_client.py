import redis


redis_client = redis.Redis(
    host="localhost",
    port=7000,
    decode_responses=True,
)