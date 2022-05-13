import socket
# https://www.youtube.com/watch?v=8A4dqoGL62E&ab_channel=sentdex
# comunication sending and receiveing bytestreams

addr = (("192.168.0.113", 5000))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET, socket.SOCK_STREAM = ipv4, tcp
s.connect(addr)
print("connected to esp")

init = "init"
end = "end"
lastIndicator = end
data = ""
logs = []
incomplete_data = []
try:
    while True:
        msg = s.recv(124)
        # print(f"msg = {msg}") # 1024 tamanho do dado em bytes
        msg = msg.decode("utf-8")
        print(f"msg = {msg}")
        if msg == init:
            if lastIndicator == end:
                data = ""
                lastIndicator = init
            else:
                incomplete_data.append(data)
                data = ""
        elif msg == end:
            logs.append(data)
            data = ""
            lastIndicator = end
        else: data += msg
except KeyboardInterrupt:
    print(logs)
    print(data)