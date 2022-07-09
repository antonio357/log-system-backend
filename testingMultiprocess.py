from time import sleep
from datetime import datetime
from multiprocessing import Process

def printExec(name):
    print(f"{name} {datetime.now().time().minute}:{datetime.now().time().second}")

def process1():
    for i in range(3):
        sleep(2)
        printExec("process1")

def process2():
    for i in range(6):
        sleep(1)
        printExec("process2")

if __name__ == "__main__":
    Process(target=process1).start()
    Process(target=process2).start()
    print("end main")
