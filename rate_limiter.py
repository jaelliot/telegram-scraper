from functools import wraps
import time
import asyncio

def rate_limited(rate_limit):
    def decorator(func):
        last_called = [0.0]

        @wraps(func)
        async def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = rate_limit - elapsed
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            result = await func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
