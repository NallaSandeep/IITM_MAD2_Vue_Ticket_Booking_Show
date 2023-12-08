from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'RedisCache',
                      'CACHE_KEY_PREFIX': 'cachekey',
                      'CACHE_REDIS_HOST': 'localhost',
                      'CACHE_REDIS_PORT': '6379',
                      'CACHE_REDIS_URL': 'redis://localhost:6379/3'})

def init_cache(app):
    cache.init_app(app)