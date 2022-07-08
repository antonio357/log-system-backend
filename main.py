import rel as autoReconn
import threading
import time
import websocket
import consts
from LogsStatus import LogsStatus

# wst = threading.Thread(target=ws.run_forever)
#     wst.daemon = True
#     wst.start()
#
#     conn_timeout = 5
#     while not ws.sock.connected and conn_timeout:
#         sleep(1)
#         conn_timeout -= 1
#
#     msg_counter = 0
#     while ws.sock.connected:
#         ws.send('Hello world %d'%msg_counter)
#         sleep(1)
#         msg_counter += 1

class LogsConn:
    def __init__(self):
        self.logsStatus = LogsStatus()
        self.ws = websocket.WebSocketApp(consts.LogsConn.URL.value,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.runThread = threading.Thread(target=self.ws.run_forever, kwargs={"dispatcher": autoReconn})
        self.runThread.daemon = True
        self.runThread.start()
        self.runThread.run()

    def sendMsg(self, msg):
        if (self.ws.sock.connected):
            self.ws.send(msg)

    def connect(self):
        self.logsStatus.reset()
        # Set dispatcher to automatic reconnection
        # self.runThread.run()
        # runs automatic reconnection
        autoReconn.dispatch()

    def close(self):
        # Interrupt rel
        autoReconn.abort()
        self.ws.close()

    def start(self):
        print("starting logs")
        self.logsStatus.reset()
        self.sendMsg(consts.LogsConn.START_LOGS_CMD.value)

    def stop(self):
        print("stoping logs")
        self.sendMsg(consts.LogsConn.STOP_LOGS_CMD.value)
        # evento de espera
        autoReconn.event(self.logsStoped())

    def logsStoped(self):
        time.sleep(1)
        print("logs stoped")
        self.logsStatus.printStatus()

    def on_message(self, ws, msg):
        log = msg
        self.logsStatus.checkMsg(log)

    def on_open(self, ws):
        print("connected to esp")
        print(f"threads active = {threading.activeCount()}")
        self.logsStatus.printStatus()

    def on_error(self, ws, error):
        print("error")
        print(f"threads active = {threading.activeCount()}")
        self.logsStatus.printStatus()

    def on_close(self, ws, close_status_code, close_msg):
        print("closed connection")
        print(f"threads active = {threading.activeCount()}")
        self.logsStatus.printStatus()


if __name__ == "__main__":
    logs = LogsConn()
    logs.connect()
    time.sleep(1)
    logs.start()
    time.sleep(4)
    logs.stop()
    print("end of main")
