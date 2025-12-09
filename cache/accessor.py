import redis


def get_redis_connection(host="localhost", port=6379, db=0) -> redis.Redis:
    client = redis.Redis(host=host, port=port, db=db)
    return client
 

def set_pomodoro_count():
    client = get_redis_connection()
    client.set("pomodoro_count", 1)