from flask import current_app


class MagpieCacheError(Exception):
    def __init__(self, err):
        logger = current_app.logger
        logger.error("CACHE ERROR: %s" % err)
        self.err = err
