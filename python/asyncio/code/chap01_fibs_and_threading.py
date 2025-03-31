import time
import threading

def print_fib(number):
    def fib(n):
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    print(f'flib({number}) is {fib(number)}')

def fibs_no_threading():
    print_fib(40)
    print_fib(41)

def fibs_with_threads():
    fortieth_thread = threading.Thread(target=print_fib, args=(40,))
    forty_first_thread = threading.Thread(target=print_fib, args=(41,))

    fortieth_thread.start()
    forty_first_thread.start()

    fortieth_thread.join()
    forty_first_thread.join()

start = time.time()

fibs_no_threading()

end = time.time()

print(f'Without threading, Completed in {end - start:.4f} seconds.')

# ---------
start = time.time()

fibs_with_threads()

end = time.time()

print(f'With threading, Completed in {end - start:.4f} seconds.')
