import threading
import time
def compte_thread1():
    conteur = 5
    while conteur > 0:
        print(f"Thread 1 : {conteur}")
        conteur -= 1
        time.sleep(1)
def compte_thread2():
    conteur = 3
    while conteur > 0:
        print(f"Thread 2 : {conteur}")
        conteur -= 1
        time.sleep(1)
t1 = threading.Thread(target=compte_thread1)
t2 = threading.Thread(target=compte_thread2)

t1.start()
t2.start()

t1.join()
t2.join()
