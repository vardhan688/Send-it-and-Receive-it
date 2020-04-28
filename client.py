import socket
#import thread
import sys

BUFFER_SIZE = 1024
IMAGE_SIZE = 5120000

PORT = int(input('Enter the port number: '))

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_IP = socket.gethostbyname(socket.gethostname())
server_IP = raw_input('Enter the server IP: ')
try:
	client_sock.connect((server_IP, PORT))
except:
	print('Error connecting to the server...')
	sys.exit()

print('You are now connected to the server')

msg = client_sock.recv(BUFFER_SIZE)
rno = str(raw_input(msg))
client_sock.send(rno)
msg = client_sock.recv(BUFFER_SIZE)
pwd = str(raw_input(msg))
client_sock.send(pwd)
flag = client_sock.recv(BUFFER_SIZE)
#flag = int(flag)
#if flag == 1:
 #   print('Youve entered an invalid password')
 #   sys.exit()

try:
    image_string = client_sock.recv(IMAGE_SIZE)
    image_file = open(rno + 'recv.png', 'wb')
    image_file.write(image_string.decode('base64'))
    image_file.close()
except:
    print('Error recieving the image..')

client_sock.close()
