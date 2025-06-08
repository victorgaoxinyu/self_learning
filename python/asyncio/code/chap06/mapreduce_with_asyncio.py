import time
import concurrent.futures
import asyncio
from collections import Counter
import functools
from typing import Dict, List
from pathlib import Path
from mapreduce import merge_dicts

filepath = Path(__file__).parent / "googlebooks-eng-all-1gram-20120701-a"

def sync_check_word_freq():
    freqs = {}

    with open(filepath.resolve(), encoding="utf-8") as f:
        lines = f.readlines()  # probably should stream

        start = time.time()
        for line in lines:
            data = line.split('\t')
            word = data[0]
            count = int(data[2])
            if word in freqs:
                freqs[word] += count
            else:
                freqs[word] = count
        
        end= time.time()
        print(f"{end - start:.4f}")  # 20 sec


def partition(data: List, chunk_size: int):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def map_freq(chunk: List[str]) -> Dict[str, int]:
    return Counter(
        {
            line.split("\t")[0]: int(line.split("\t")[2])
            for line in chunk
        }
    )
    # counter = {}
    # for line in chunk:
    #     word, _, count, _ = line.split('\t')
    #     if counter.get(word):
    #         counter[word] += int(count)
    #     else:
    #         counter[word] = int(count)

    # return counter

async def async_check_word_freq(partition_size: int):
    with open(filepath.resolve(), encoding="utf-8") as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()

        with concurrent.futures.ProcessPoolExecutor() as pool:
            for chunk in partition(contents, partition_size):
                tasks.append(loop.run_in_executor(pool, functools.partial(map_freq, chunk)))
            
            intermediate_results = await asyncio.gather(*tasks)
            final_result = functools.reduce(merge_dicts, intermediate_results)

        end = time.time()

        print(f"Async took: {end - start:.4f}")


if __name__ == "__main__":
    # sync_check_word_freq()
    asyncio.run(async_check_word_freq(partition_size=60000))
