import threading
from queue import Queue
import time

print_lock = threading.Lock()  # prevents interposing voices

def Job(worker):
    time.sleep(1)  # the simulated task
    with print_lock:
        print(threading.current_thread().name, worker)

# performs threading operation
def threader():
    while True:
        worker = q.get()
        Job(worker)
        q.task_done()

q = Queue()
# makes workers
for i in range(10):
    t = threading.Thread(target=threader)
    t.daemon = True  # classified as daemon, so it dies when the main thread does
    t.start()

start = time.time()

# makes jobs
for worker in range(20):
    q.put(worker)

q.join()  # blocks until all workers have been gotten and done
print("Job took:", time.time() - start)

# https://www.youtube.com/watch?v=NwH0HvMI4EA&list=PLQVvvaa0QuDe8XSftW-RAxdo6OmaeL85M&index=45
# https://docs.python.org/2/library/queue.html
