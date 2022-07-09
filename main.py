import time
from time import sleep
from datetime import datetime
from sniffer_logs_connection import SnifferLogsConnection
from threading import Thread

# this function is just for testing
def stopSnifferLogsAfterSeconds(snifferLogsConnection, seconds=5):
    sleep(seconds)
    snifferLogsConnection.stopLogs()

if __name__ == "__main__":
    snifferLogsConnection = SnifferLogsConnection()
    snifferLogsConnectionThread = Thread(target=snifferLogsConnection.connect)
    snifferLogsConnectionThread.start()
    snifferLogsConnection.startLogs()

    # this line is just for testing
    Thread(target=stopSnifferLogsAfterSeconds,
           kwargs={"snifferLogsConnection": snifferLogsConnection}).start()

    while True:
        sleep(1)
        print(f"\nMain thread: {datetime.now()}\n")
