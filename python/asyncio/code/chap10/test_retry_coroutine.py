import asyncio
from retry_coroutine import retry, TooManyRetries


async def main():
    async def always_fail():
        raise Exception('I have failed!')
    
    async def always_timeout():
        await asyncio.sleep(1)
    
    try:
        await retry(always_fail, max_retries=3, timeout=.1, retry_interval=.1)
    except TooManyRetries:
        print("Retried too many times!")

    try:
        await retry(always_timeout, max_retries=3, timeout=.1, retry_interval=.1)
    except TooManyRetries:
        print("Retried too many times!")


asyncio.run(main())