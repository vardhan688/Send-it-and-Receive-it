#import getpass
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#import time
import socket
import threading
import sys
import base64

URL = 'https://ecampus.psgtech.ac.in/studzone/AttWfStudMenu.aspx'
academic = 'Title1_Menu1-menuItem002'
Rollno = 'Txtstudid'
Password = 'TxtPasswd'
CA_Marks = 'Title1_Menu1-menuItem002-subMenu-menuItem004'
sign_out = 'Title1_LkbSignOut'

IMAGE_SIZE = 5120000
BUFFER_SIZE = 1024
clients = []
lock = threading.Lock()

def sendImage(client_sock, rno):
    file_name = (rno + '.png')
    try:
        with open(file_name, 'rb') as image_file:
            image_string = base64.b64encode(image_file.read())
            client_sock.send(image_string)
    except:
        print('Error transmitting the file..')

def fetchData(addr, rno, pwd):
    #flag = 0
    browser = webdriver.Firefox()
    #browser.set_window_position(2000,2000)
    browser.get(URL)
    action = ActionChains(browser)
    username = browser.find_element_by_id(Rollno)
    password = browser.find_element_by_id(Password)
    username.send_keys(rno)
    password.send_keys(pwd)
    browser.find_element_by_xpath("//*[@type='submit']").click()
    try:
        Menu = browser.find_element_by_id(academic)
        action.move_to_element(Menu).perform();
        CA_Marks_Menu = browser.find_element_by_id(CA_Marks)
        CA_Marks_Menu.click();
        browser.save_screenshot(rno + '.png')
        browser.find_element_by_id(sign_out).click()
        browser.close()
        #client_sock.send(flag)
    except:
        print(addr[0] + ' has entered an invalid password')
        #flag = 1
        #client_sock.send(str(flag))
        browser.close()
        sys.exit()

def handleClient (client_sock, addr):
    print('Connected by ' + addr[0])
    #clients.append(client_sock)
    client_sock.send('Enter your Rollno: ')
    rno = client_sock.recv(BUFFER_SIZE)
    client_sock.send('Enter your password: ')
    #pass = getpass.getpass('Enter your Password: ')
    pwd = client_sock.recv(BUFFER_SIZE)
    fetchData(addr, rno, pwd)
    sendImage(client_sock, rno)
    client_sock.close()

PORT = int(input('Enter the port number: '))
server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_IP = socket.gethostbyname(socket.gethostname())

server_sock.bind((server_IP, PORT))

print('Server IP is ' + server_IP)

server_sock.listen(10)

while True:
    client_sock, addr = server_sock.accept()
    try:
        client_thread = threading.Thread(target = handleClient , args = [client_sock, addr])
        clients.append( client_thread )
        clients[len(clients)-1].start()
        #handleClient(client_sock, addr)
    except:
        print('Error handling client...')
        client_sock.close()
        sys.exit()
    #client_sock.close()
server_sock.close()
