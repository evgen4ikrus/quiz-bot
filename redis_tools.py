import redis


def auth_redis(redis_address, redis_port, redis_password):
    redis_obj = redis.Redis(host=redis_address, port=redis_port, password=redis_password,
                            charset='utf-8', decode_responses=True)
    return redis_obj
