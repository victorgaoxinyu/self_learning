from threading import Lock, Thread
import time

lock_a = Lock()
lock_b = Lock()

def a():
    with lock_a:
        print("Acquired lock A from method A")
        time.sleep(1)
        with lock_b:
            print("Acquired both locks from method A")

def b():
    with lock_b:
        print("Acquired lock B from method B")
        with lock_a:
            print("Acquired both locks from method B")


thread_a = Thread(target=a)
thread_b = Thread(target=b)

thread_a.start()
thread_b.start()

thread_a.join()
thread_b.join()


