import websocket, time, rel

ip, port = ("192.168.0.113", 81)
adrr = f"{ip}:{port}"
url = f"ws://{adrr}"

def current_milli_time():
    return round(time.time() * 1000)

msgs = []
corrupted_msgs = []
last_time = current_milli_time()
def on_message(ws, msg):
    global last_time
    now = current_milli_time()
    response_time = now - last_time
    if len(msg) == 256: msgs.append((msg, response_time))
    else: corrupted_msgs.append((msg, response_time))
    last_time = now

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Connected to esp")

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

mean_time = (sum([i[-1] for i in msgs]) + sum([i[-1] for i in corrupted_msgs])) / (len(msgs) + len(corrupted_msgs))
print(f"received msgs: {len(msgs)} corrupted_msgs: {len(corrupted_msgs)} mean time: {mean_time}")

# https://github.com/websocket-client/websocket-client