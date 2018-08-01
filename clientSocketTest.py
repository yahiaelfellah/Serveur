import socket,sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print(e)
    sys.exit()
print("Socket Created.........")
host = "192.168.8.100"
port = 8888
try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print("Hostname could not be resolved....")
    sys.exit()
s.connect((host,port))
print("We are connected ... ")
# Data to send
message = b''
while len(message) <= 4096*8 :
    message = message + b'The tempfile module also provides a NamedTemporaryFile '
print(len(message))
try:
    s.sendall(message)
except socket.error:
    print("Error of sending ....")
    sys.exit()
print("Message send ....")

