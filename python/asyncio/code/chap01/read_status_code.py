import time
import threading
import requests

def read_example():
    response = requests.get('https://www.example.com')
    print(response.status_code)

sync_start = time.time()

read_example()
read_example()

sync_end = time.time()

print(f'Running synchronously took {sync_end - sync_start:.4f} seconds.')

thread1 = threading.Thread(target=read_example)
thread2 = threading.Thread(target=read_example)

thread_start = time.time()
thread1.start()
thread2.start()

print('All threads running')

thread1.join()  # block the main thread
thread2.join()  # will only contionue execute if thread1 and thread2 complete

thread_end = time.time()

print(f'Running with threads took {thread_end - thread_start:.4f} seconds.')
