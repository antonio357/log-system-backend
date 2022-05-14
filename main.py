import socket, re
# https://www.youtube.com/watch?v=8A4dqoGL62E&ab_channel=sentdex
# comunication sending and receiveing bytestreams

#https://www.youtube.com/watch?v=tGR5zqN9M2E&ab_channel=datasith

addr = (("192.168.0.113", 5000))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET, socket.SOCK_STREAM = ipv4, tcp
s.connect(addr)
print("connected to esp")

max_len = 9999
message_header = "log-header:9999."
message_header_len = 17
data = ""
logs = []
corrupted_logs = []
incomplete_data = []



log_data = ""
log_header_len = 16
log_header = ""


class getHeader:
    def __init__(self, header='', headerMask="log-header:dddd."):
        self.header = header
        self.headerMask = headerMask
        self.headerLen = len(self.headerMask)

    def mountHeader(self, msg):
        for i in range(len(msg)):
            char = msg[i]
            expectedChar = self.headerMask[len(self.header)]
            if expectedChar == '.':
                dataLen, dataBeginIndex = int(re.findall(r'\d+', self.header)[0]), i + 1
                print(self.header)
                self.header = ''
                return (dataLen, dataBeginIndex)
            if expectedChar == 'd' or char == expectedChar:
                self.header += char
            else: self.header = ''
        return (None, None)

getheader = getHeader()
left = ''
try:
    while True:
        s.connect(addr)
        msg = s.recv(128).decode("utf-8")
        dataLen, dataBeginIndex = getheader.mountHeader(left + msg)
        left = ''
        if dataBeginIndex:
            log_data += msg[dataBeginIndex:]
            while len(log_data) < dataLen:
                msg = s.recv(128).decode("utf-8")
                if len(log_data) + len(msg) <= dataLen:
                    log_data += msg
                else:
                    log_data += msg[:dataLen - len(log_data)]
                    left = msg[dataLen - len(log_data):]
                    if len(log_data) == dataLen:
                        logs.append(log_data)
                    else:
                        corrupted_logs.append(log_data)
                    print(log_data)
                    log_data = ""

except KeyboardInterrupt:
    pass
    # print(logs)
    # print(data)
finally:
    print(f"logs = {len(logs)}, corrupted_logs = {len(corrupted_logs)}, all_data = {len(logs) + len(corrupted_logs)}")
    print(f"logs = {logs}, corrupted_logs = {corrupted_logs}")
