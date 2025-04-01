import multiprocessing
import os
import time
import subprocess

def worker(number):
    pid = os.getpid()
    # core = os.sched_getaffinity(0)  # this line does not work under macos
                                      # macos does not have public API to getch the current core number
                                      # Fark!

    cpu_info = subprocess.check_output(["ps", "-p", str(pid), "-o", "%cpu"]).decode().strip().split("\n")[-1]
    
    print(f'Worker {number} running with PID {pid} on CPU core(s): {cpu_info}')
    time.sleep(2)

if __name__ == "__main__":
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=worker, args=(i, ))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

    print('All processes completed.')