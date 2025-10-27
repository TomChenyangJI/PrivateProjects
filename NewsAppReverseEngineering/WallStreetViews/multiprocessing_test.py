from multiprocessing import Pool, Lock, Value, Queue

#
# li = []
#
#
# # lock = Lock()
#
#
# def ini(v):
#     global val
#     # li = l
#     val = v
#
# def t(v):
#     # li.append(v)
#     # val = 2
#     # print(v)
#     # print(li)
#     val += v
#     print(val)
#     with val.get_lock():
#         val.value += 1
#         print(f"{val.value=}")
#
# if __name__ == "__main__":
#     val = Value('d', 0)
#     with Pool(10, initializer=ini, initargs=(val,)) as p:
#         p.map(t, (1, 2, 3, 4, 5))
#     print(li)


# def test(i):
#     with profit.get_lock():
#         profit.value += 1
#         print(f"{profit.value=}")
#
# def test_iter(e):
#     for i in range(e):
#         yield i
#
# def init(v):
#     global profit
#     profit = v
#
# if __name__ == "__main__":
#     profit = Value('d', 0)
#     for i in range(30):
#         with Pool(10, initializer=init, initargs=(profit, )) as p:
#             p.map(test, test_iter(100))


# def init(v):
#     global val
#     val = v
#     print(f"{val.value=}")
#
# def t(i):
#     with val.get_lock():
#         val.value += 1
#         print("--", val.value)
#
#
# if __name__ == "__main__":
#     val = Value('d', 0)
#
#     with Pool(10, initializer=init, initargs=(val, )) as p:
#         p.map(t, range(100))


def init(l, li_obj, q):
    global lock, li, qu
    lock = l
    li = li_obj
    qu = q

def t(v):
    global li
    lock.acquire()
    li.append(v)
    print(li)
    qu.put(v)
    lock.release()



if __name__ == "__main__":
    li = []
    lock = Lock()
    qu = Queue()

    with Pool(12, initializer=init, initargs=(lock, li, qu)) as p:
        p.map(t, range(100))

    while not qu.empty():
        print(qu.get())
