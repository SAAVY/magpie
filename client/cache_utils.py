from cache.connection import RedisInstance as Redis


def is_redis_available():
    return Redis.redis_instance.is_available()  # getting None returns None or throws an exception


def cache_json_data(url, data):
    Redis.redis_instance.cache_url(url, data)


def get_cached_data(url):
    return Redis.redis_instance.get_cached_data(url)
