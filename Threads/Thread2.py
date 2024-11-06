import threading
import time
def countdown_thread1():
    count = 5
    while count > 0:
        print(f"Thread 1 : {count}")
        count -= 1
        time.sleep(1)
def countdown_thread2():
    count = 3
    while count > 0:
        print(f"Thread 2 : {count}")
        count -= 1
        time.sleep(1)
t1 = threading.Thread(target=countdown_thread1)
t2 = threading.Thread(target=countdown_thread2)

t1.start()
t2.start()

t1.join()
t2.join()
