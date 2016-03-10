import cProfile
import pstats

from config import config


def cprofile(func):
    def profiled_func(*args, **kwargs):
            profile = cProfile.Profile()
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                return result
            finally:
                stats = pstats.Stats(profile)
                stats.strip_dirs().sort_stats('cumulative').print_stats(20)

    if config.IS_DEV and config.PROFILE_METHODS:
        return profiled_func
    else:
        return func
