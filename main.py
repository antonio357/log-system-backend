from time import sleep
from datetime import datetime
from sniffer_logs_connection import SnifferLogsConnection


if __name__ == "__main__":
    snifferLogsConnection = SnifferLogsConnection()
    for i in range(2):
        snifferLogsConnection.startLogs()
        sleep(8)
        snifferLogsConnection.stopLogs()
        sleep(60*10)

    # react https://www.youtube.com/watch?v=azvcvbeRZ08&ab_channel=WebDevJunkie ->
    # https://github.com/codyseibert/youtube/tree/master/realtime-chart-websockets
    # while True:
    #     sleep(1)
    #     print(f"\nMain thread: {datetime.now()}\n")
