import socket
import time
import struct

addr = (("192.168.4.1", 5000))


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(addr)

msg = bytearray()
for i in range(6): msg.append(48 + i)

for i in range(6): client_socket.send(chr(msg[i]).encode())

time.sleep(1)

client_socket.close()