from consts import LogsConn
from logs_status import LogsStatus
from websocket import WebSocketApp
from threading import Thread
from time import sleep, time
import rel as autoReconnect
import asyncio

class SnifferLogsConnection:
    def __init__(self, lifeTimeSeconds=None):
        self._name = "sniffer"
        self._logsStatus = LogsStatus()

        self._websocket = None
        self.connect()

        # lifeTimeSeconds is just for tests
        if lifeTimeSeconds:
            Thread(target=self._stopLogsAfterSeconds, kwargs={"seconds": lifeTimeSeconds}).start()

    def connect(self):
        if not self._isConnected():
            self._thread = Thread(target=self._runConnection)
            self._thread.start()
            self._waitConnection()

    def _runConnection(self):
        self._websocket = WebSocketApp(LogsConn.URL.value,
                                      on_open=self._onOpen,
                                      on_message=self._onMessage,
                                      on_error=self._onError,
                                      on_close=self._onClose)

        self._websocket.run_forever(dispatcher=autoReconnect)
        autoReconnect.dispatch()

    def _waitConnection(self):
        startTime = self._nowTimeInSeconds()
        while not self._isConnected():
            if self._nowTimeInSeconds() - startTime > 5:
                raise TimeoutError(f"{self._name} error: took more than 5 seconds to connect")

    def _isConnected(self):
        if self._websocket and self._websocket.sock.connected:
            return True
        return False

    def closeConnection(self):
        autoReconnect.abort()
        self._websocket.close()

    def _onOpen(self, websocket):
        self._printStrings("connected")
        self._logsStatus.printStatus()

    def _onMessage(self, websocket, message):
        self._logsStatus.checkMsg(message)

    def _onError(self, websocket, error):
        self._printStrings("error")
        self._logsStatus.printStatus()

    def _onClose(self, websocket, close_status_code, close_message):
        self._printStrings(f"closed connection with " 
                           f"close_status_code = {close_status_code}, "
                           f"close_message = {close_message}")
        self._logsStatus.printStatus()

    def startLogs(self):
        self._printStrings("starting logs")
        self._logsStatus.reset()
        self._websocket.send(LogsConn.START_LOGS_CMD.value)

    def stopLogs(self):
        self._printStrings("stopping logs")
        self._websocket.send(LogsConn.STOP_LOGS_CMD.value)
        Thread(target=self._waitLatestLogs).start()

    def _waitLatestLogs(self):
        sleep(1)
        self._logsStatus.printStatus()

    def _nowTimeInSeconds(self):
        return int(time())

    # test is just for tests
    def _stopLogsAfterSeconds(self, seconds):
        sleep(seconds)
        self.stopLogs()

    def _printStrings(self, string):
        print(f"{self._name} {string}")