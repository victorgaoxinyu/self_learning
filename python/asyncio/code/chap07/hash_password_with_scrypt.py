import hashlib
import functools
import asyncio
import os
import string
import time
import random
from concurrent.futures.thread import ThreadPoolExecutor

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from util import async_timed, delay

def random_password(length: int) -> bytes:
    ascii_lowercase = string.ascii_lowercase.encode()
    return b''.join(bytes(random.choice(ascii_lowercase)) for _ in range(length))

passwords = [random_password(10) for _ in range(10000)]

def hash_p(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


def compute_normally():
    start_time = time.time()

    for password in passwords:
        hash_p(password)

    print(time.time() - start_time)  # 20 sec

@async_timed()
async def compute_with_multithread():
    loop = asyncio.get_running_loop()
    tasks = []

    with ThreadPoolExecutor() as pool:
        for password in passwords:
            tasks.append(loop.run_in_executor(pool, functools.partial(hash_p, password)))

    await asyncio.gather(*tasks)  # 3 sec

if __name__ == "__main__":
    # compute_normally()
    asyncio.run(compute_with_multithread())
