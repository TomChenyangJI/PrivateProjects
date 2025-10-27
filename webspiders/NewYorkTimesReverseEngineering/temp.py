from multiprocessing import Pool, Lock, Queue
import random

def t(li):
    i = random.randint(1, 10)
    if i == 2:
        lock.acquire()
        que.put({i: i})
        print(i)
        lock.release()
    print('done')

def iter(li):
    for i in range(100):
        yield li

def init(l, q):
    global lock, que
    lock = l
    que = q


if __name__ == "__main__":
    li = []
    lock = Lock()
    que = Queue()
    with Pool(20, initializer=init, initargs=(lock, que)) as p:
        p.map(t, iter(li))
    # print(list(que))
    while not que.empty():
        print(que.get())
        # continue