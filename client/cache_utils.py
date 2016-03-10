import redis

from cache.connection import RedisInstance as Redis


def is_redis_available():
    try:
        Redis.redis_instance.get(None)  # getting None returns None or throws an exception
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return False
    return True


def cache_json_data(url, data):
    Redis.redis_instance.cache_url(url, data)


def get_cached_data(url):
    return Redis.redis_instance.get_cached_data(url)
