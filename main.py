from time import sleep, localtime
from datetime import datetime
from ws import startConn, startLogs, stopLogs, stopLogsAfter

if __name__ == "__main__":
    logsCoonId = startConn()
    startLogs()
    stopLogsAfter(5)
    while True:
        sleep(1)
        print(f"\nMain thread: {datetime.now()}\n")
