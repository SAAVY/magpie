# set debug to False on non prod env
IS_DEV = True

# profile speed of methods and output it to terminal
PROFILE_METHODS = False

# set to false if you want to disable accessing redis
CACHE_DATA = False

MAX_DESC_LENGTH = 200


class ImageAttrs(object):
    MIN_IMAGE_HEIGHT = 50
    MIN_IMAGE_WIDTH = 50
    MAX_RETURN_IMAGES = 10
