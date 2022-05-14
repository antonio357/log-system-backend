import socket
# https://www.youtube.com/watch?v=8A4dqoGL62E&ab_channel=sentdex
# comunication sending and receiveing bytestreams

addr = (("192.168.0.113", 5000))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET, socket.SOCK_STREAM = ipv4, tcp
s.connect(addr)
print("connected to esp")

max_len = 9999
message_header = "log-header:9999."
message_header_len = 17
data = ""
logs = []
incomplete_data = []



log_data = ""
log_header_len = 16
log_header = ""

try:
    while True:
        # reading log_header
        msg = s.recv(message_header_len).decode("utf-8")
        diff = log_header_len - len(log_header)
        log_header += msg[:diff]
        log_data += msg[diff:] # header and data may mix
        if len(log_header) == log_header_len or len(log_data) > 0: # reading data
            print(f"log_header = {log_header}")
            expected_len = int(log_header.replace('.', '')[11:]) - len(log_data)
            log_data += s.recv(expected_len).decode("utf-8")
            # in the end
            logs.append(log_data)
            log_data = ""
            log_header = ""

except KeyboardInterrupt:
    pass
    # print(logs)
    # print(data)
finally:
    print(f"logs received = {len(logs)}")