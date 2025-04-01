def consumer():
    r = ''
    while True:
        n = yield r
        if not n :
            return
        print(f'[CONSUMER] Consuming {n}')
        r = f'200 OK from iter {n}'

def produce(c):
    # c.send(None)
    next(c)
    n = 0
    while n < 5:
        n = n + 1
        print(f'[PRODUCER] Producing {n}')
        r = c.send(n)
        print(f'[PRODUCER] Consumer return: {r}')
    
    c.close()

c = consumer()
produce(c)
        
