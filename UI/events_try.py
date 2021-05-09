import threading
import time


def thread2(ev: threading.Event()):
    print('entering second thread')
    while ev.isSet():
        pass
    print('second thread end')


def thread1(ev: threading.Event):
    print('entering first thread...')
    time.sleep(3)
    ev.clear()
    print('event was cleared, exiting first thread')


eve = threading.Event()
eve.set()
t1 = threading.Thread(target=thread1, args=(eve,))
t2 = threading.Thread(target=thread2, args=(eve,))
t1.start()
t2.start()
# t1.join()
# t2.join()
