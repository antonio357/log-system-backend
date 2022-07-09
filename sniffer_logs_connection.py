from consts import LogsConn
from logs_status import LogsStatus
from websocket import WebSocketApp
from threading import Thread
from time import sleep, time

class SnifferLogsConnection:
    def __init__(self):
        self.logsStatus = LogsStatus()
        self.websocket = None
        self.name = "sniffer"
        self.startTime = None

    def connect(self):
        print(f"{self.name} beginning of connect")
        self.websocket = WebSocketApp(LogsConn.URL.value,
                                      on_open=self.onOpen,
                                      on_message=self.onMessage,
                                      on_error=self.onError,
                                      on_close=self.onClose)
        print(f"{self.name} running of connect")
        self.websocket.run_forever()
        print(f"{self.name} end of connect")

    def isConnected(self):
        if self.websocket and self.websocket.sock.connected:
            return True
        return False

    def closeConnection(self):
        self.websocket.close()

    def startLogs(self):
        print(f"{self.name} starting logs")
        self.logsStatus.reset()
        startTime = self.nowTimeInSeconds()
        while not self.isConnected():
            self.connectingTimeOut(startTime)
        self.websocket.send(LogsConn.START_LOGS_CMD.value)

    def stopLogs(self):
        print(f"{self.name} stoping logs")
        self.websocket.send(LogsConn.STOP_LOGS_CMD.value)
        Thread(target=self.waitLatestLogs).start()

    def waitLatestLogs(self):
        sleep(2)
        self.logsStatus.printStatus()

    def onMessage(self, websocket, message):
        self.logsStatus.checkMsg(message)

    def onOpen(self, websocket):
        print(f"{self.name} connected")
        self.logsStatus.printStatus()

    def onError(self, websocket, error):
        print(f"{self.name} error")
        self.logsStatus.printStatus()

    def onClose(self, websocket, close_status_code, close_message):
        print(f"{self.name} closed connection with close_status_code = {close_status_code}, close_message = {close_message}")
        self.logsStatus.printStatus()

    def nowTimeInSeconds(self):
        return int(time())

    def connectingTimeOut(self, startTime):
        if self.nowTimeInSeconds() - startTime > 5:
            raise Exception(f"{self.name} took to long to connect")
