import redis

from data import MagpieData
from exceptions import MagpieCacheError


class RedisInstance(object):

    redis_instance = None

    def _establish_db_connection(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)  # db=0 denotes the default redis database.
        self.redis = redis.StrictRedis(connection_pool=self.pool)

    def __init__(self):
        try:
            self._establish_db_connection()
        except Exception, err:
            raise MagpieCacheError(err)

    def cache_url(self, url, data):
        self.redis.set(url, data)

    def get_cached_data(self, url):
        data = self.redis.get(url)
        if data is None:
            return None
        return MagpieData(url, data)

    @staticmethod
    def init_redis_instance():
        RedisInstance.redis_instance = RedisInstance()
