# Import WebSocket client library (and others)
import websocket
import threading
import _thread
import time

counter = 0
# Define WebSocket callback functions
def ws_message(ws, message):
    global counter
    counter = counter + 1
    if (counter > 5000): ws.send('stop logs')
    print("WebSocket thread: %s" % counter)

def ws_open(ws):
    global counter
    counter = 0
    ws.send('start logs')

def ws_thread(*args):
    ws = websocket.WebSocketApp("ws://192.168.1.199:81", on_open=ws_open, on_message=ws_message)
    ws.run_forever()
    print("got here")

# Start a new thread for the WebSocket interface
# _thread.start_new_thread(ws_thread, ())
threading.Thread(target=ws_thread).start()
# Continue other (non WebSocket) tasks in the main thread
while True:
    time.sleep(1)
    print("Main thread: %d" % time.time())


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