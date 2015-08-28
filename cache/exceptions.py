class MagpieCacheError(Exception):
    def __init__(self, err):
        # TODO: Log "MAGPIE CACHE ERROR: %s" % err
        print "MAGPIE CACHE ERROR: %s" % err
        self.err = err
