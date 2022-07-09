from time import sleep
from datetime import datetime
from sniffer_logs_connection import SnifferLogsConnection


if __name__ == "__main__":
    snifferLogsConnection = SnifferLogsConnection(lifeTimeSeconds=5)
    snifferLogsConnection.startLogs()

    while True:
        sleep(1)
        print(f"\nMain thread: {datetime.now()}\n")
