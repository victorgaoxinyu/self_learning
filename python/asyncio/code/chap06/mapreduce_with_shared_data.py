from concurrent.futures import ProcessPoolExecutor
import functools
import asyncio
from multiprocessing import Value
from typing import List, Dict
from mapreduce import merge_dicts
from mapreduce_with_asyncio import partition
from collections import Counter
from pathlib import Path

map_progress: Value
filepath = Path(__file__).parent / "googlebooks-eng-all-1gram-20120701-a"


def init(progress: Value):
    global map_progress
    map_progress = progress


def map_freq(chunk: List[str]) -> Dict[str, int]:
    counter = Counter(
        {
            line.split("\t")[0]: int(line.split("\t")[2])
            for line in chunk
        }
    )

    with map_progress.get_lock():
        map_progress.value += 1
    
    return counter


async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f"Finished {map_progress.value}/{total_partitions} map operations")
        await asyncio.sleep(1)
    

async def main(partition_size: int):
    global map_progress
    with open(filepath.resolve()) as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        map_progress = Value("i", 0)

        with ProcessPoolExecutor(initializer=init, initargs=(map_progress, )) as pool:
            total_partitions = len(contents) // partition_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))
            for chunk in partition(contents, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        pool, functools.partial(map_freq, chunk)
                    )
                )
            counters = await asyncio.gather(*tasks)

            await reporter

            final_result = functools.reduce(merge_dicts, counters)

            print(f"Aardvark has appeared {final_result['Aardvark']} times")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))