import math, threading

print_lock = threading.Lock()
prime_lock = threading.Lock()
prime = True # until proven otherwise

possibleprime = int(input("Prime Check\n>> "))

if str(possibleprime)[-1] in [1,3,7,9]:
    def primecheck(lo, hi):
        i = lo
        while i < hi and prime:
            if possibleprime % i == 0:
                with prime_lock:
                    prime = False
                    
    # makes workers
    for i in range(2, int(math.ceil(possibleprime/2.0))):  # how many workers available
        t = threading.Thread(target=primecheck)  # put workers to work
        t.daemon = True
        t.start()
else:
    with prime_lock:
        prime = False
        
if prime:
    with print_lock:
        print("Prime")
else:
    with print_lock:
        print("Not Prime")
