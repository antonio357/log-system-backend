from websocket import WebSocketApp
from _thread import start_new_thread
from consts import LogsConn
from LogsStatus import LogsStatus
from time import sleep


ws = None
allLogsReceived = True
name = "logs connection"
logsStatus = LogsStatus()

def onMsg(ws, msg):
    logsStatus.checkMsg(msg)

def onErr(ws, err):
    global allLogsReceived
    allLogsReceived = True
    print(f"{name} error = {err}")

def onClose(ws, status_code, msg):
    global allLogsReceived
    allLogsReceived = True
    print(f"{name} closed with status_code = {status_code}, msg = {msg}")

def onOpen(ws):
    global allLogsReceived
    allLogsReceived = True
    print(f"{name} opened")

def connect():
    global ws
    ws = WebSocketApp(LogsConn.URL.value,
                      on_open=onOpen,
                      on_message=onMsg,
                      on_error=onErr,
                      on_close=onClose)
    ws.run_forever()

def startConn():
    return start_new_thread(connect, ())

def wsIsConnected():
    global ws
    if ws and ws.sock.connected:
        return True
    return False

def startLogs():
    global ws, allLogsReceived
    while not wsIsConnected(): continue
    logsStatus.reset()
    allLogsReceived = False
    print(f"{name} starting logs")
    ws.send(LogsConn.START_LOGS_CMD.value)

def waitLastsLogs():
    global allLogsReceived
    sleep(2)
    allLogsReceived = True
    logsStatus.printStatus()

def stopLogs():
    global ws
    if wsIsConnected():
        print(f"{name} stoping logs")
        ws.send(LogsConn.STOP_LOGS_CMD.value)
        start_new_thread(waitLastsLogs, ())

def makeThreadWait(s):
    sleep(s)
    stopLogs()

def stopLogsAfter(s):
    start_new_thread(makeThreadWait, (s,))
