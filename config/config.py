# set debug to False on non prod env
IS_DEV = False

# port for development configuration
DEV_PORT = 5000

# profile speed of methods and output it to terminal
PROFILE_METHODS = False

# set to false if you want to disable accessing redis
CACHE_DATA = False

# set default max description length
MAX_DESC_LENGTH = 200


# set default image return attributes
class ImageAttrs(object):
    MIN_IMAGE_HEIGHT = 50
    MIN_IMAGE_WIDTH = 50
    MAX_RETURN_IMAGES = 10

# host redis is on, default to localhost
REDIS_HOST = '127.0.0.1'

# port redis is on
REDIS_PORT = '6379'

# global limit for rate limiter; see http://flask-limiter.readthedocs.org/en/stable/#ratelimit-string
# for formatting
GLOBAL_RATE_LIMIT = ["100/minute", "5/second"]
