import secrets


async def set_get_token(redis, user_id):
    token = secrets.token_hex()
    await redis.set('user_token:%s' % token, user_id)
    await redis.expire('user_token:%s' % token, 60 * 60 * 30)

    return token