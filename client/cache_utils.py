from cache.connection import RedisInstance as Redis


def cache_url(url, data):
    Redis.redis_instance.cache_url(url, data)


def get_cached_data(url):
    return Redis.redis_instance.get_cached_data(url)
