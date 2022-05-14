import websocket
import _thread
import time
import rel


ip, port = ("192.168.0.113", 81)
adrr = f"{ip}:{port}"
url = f"ws://{adrr}"

counter = 0
def on_message(ws, message):
    global counter
    print(f"message num {counter}")
    counter = counter + 1

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

# https://github.com/websocket-client/websocket-client