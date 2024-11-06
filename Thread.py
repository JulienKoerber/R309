import threading
import time
def thread1():
    for i in range(5):
        print("Je suis la thread 1")
        time.sleep(0.5)

def thread2():
    for i in range(5):
        print("Je suis la thread 2")
        time.sleep(0.5)

t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

t1.start()
t2.start()

t1.join()
t2.join()
