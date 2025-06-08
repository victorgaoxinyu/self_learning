import time
import functools
from typing import Dict, List




def map_freq(text: str) -> Dict[str, int]:
    words = text.split(' ')
    freq_dict = {}
    for word in words:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    
    return freq_dict


def merge_dicts(first, second):
    merged = first
    for key in second:
        if key in merged:
            merged[key] += second[key]
        else:
            merged[key] = second[key]

    return merged

if __name__ == "__main__":

    lines = ["I know what I know",
            "I know that I know",
            "I don’t know that much",
            "They don’t know much"]

    mapped_results = [map_freq(line) for line in lines]

    for result in mapped_results:
        print(result)

    print(functools.reduce(merge_dicts, mapped_results))
