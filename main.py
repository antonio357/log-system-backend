from time import sleep
from datetime import datetime
from sniffer_logs_connection import SnifferLogsConnection


if __name__ == "__main__":
    snifferLogsConnection = SnifferLogsConnection()
    for i in range(3):
        snifferLogsConnection.startLogs()
        sleep(5)
        snifferLogsConnection.stopLogs()
        sleep(1)

    snifferLogsConnection.closeConnection()
    snifferLogsConnection.connect()

    for i in range(3):
        snifferLogsConnection.startLogs()
        sleep(5)
        snifferLogsConnection.stopLogs()
        sleep(1)

    snifferLogsConnection.closeConnection()
    del snifferLogsConnection

    # react https://www.youtube.com/watch?v=azvcvbeRZ08&ab_channel=WebDevJunkie ->
    # https://github.com/codyseibert/youtube/tree/master/realtime-chart-websockets
    # while True:
    #     sleep(1)
    #     print(f"\nMain thread: {datetime.now()}\n")
