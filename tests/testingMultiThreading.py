from time import sleep
from datetime import datetime
from threading import Thread

def printExec(name):
    print(f"{name} {datetime.now().time().minute}:{datetime.now().time().second}")

def thread1():
    for i in range(3):
        sleep(2)
        printExec("thread1")

def thread2():
    for i in range(6):
        sleep(1)
        printExec("thread2")

if __name__ == "__main__":
    Thread(target=thread1).start()
    Thread(target=thread2).start()
    print("main end")
