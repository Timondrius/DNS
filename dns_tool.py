
import subprocess
import socket
from urllib import request, error
from ftplib import FTP
#TASK 1
def execute(command, domain):
  return subprocess.run([command, domain], capture_output=True, text = True).stdout
#TASK 2
def http_request(target_url):
  try:
    with request.urlopen(target_url) as response:
      return f"Status: {response.getcode()}\n{response.read().decode('utf-8')}"
  except error.URLError as e:
    return e

def ftp_transfer(server, port):
  ftp = FTP()
  ftp.connect(server, port)
  user = input("Enter username for ftp connection or None:")
  password = input("Enter password for ftp connection or None:")
  try:
    if(user != "None" and password != "None"):
      ftp.login(user, password)
    else:
      ftp.login()
    return "You are connectrd successfully"
  except Exception as e:
    return e

#TASK 4
def tcp_client(socket, request):
  socket.sendall(request.encode("utf-8"))
  return socket.recv(1024).decode("utf-8")

def upd_client(socket, request):
  socket.sendto(request.encode("utf-8"), ("localhost", 8080))
  return socket.recvfrom(1024).decode("utf-8")
  
  
  
def task4():
  while True:
    type = input("Please enter tcp, udp or exit ")
    if(type == "tcp"):
      server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server.bind(('localhost', 8080))
      server.listen(5)
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect(('localhost', 8080))
      print(f"Connected to server at {client.getsockname()}")
      r = input("Please enter the request ")
      client, address = server.accept()
      conn, addr = server.accept()
      print(f"{address} connected")

      response = tcp_client(client, r)
    elif(type == "udp"):
      server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      server.bind(('localhost', 8080))
      server.listen(5)
      client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      client.connect(('localhost', 8080))
      print(f"Connected to server at {client.getsockname()}")
      r = input("Please enter the request ")
      client, address = server.accept()
      response = udp_client(client, r)
    else:
      print("Exiting..")
      return
    print(response)
  



while(True):
  dnscommand = input("Enter your DNS command\n e for exit \n n for nslookup \n h for host \n d for dig \n req for http request \n transfer for ftp transfer \n or protocol for udp client or tcp server: ")

  if dnscommand == 'n':
    domain = input("Enter the domain name: ")
    result = execute("nslookup", domain)
  elif dnscommand == 'h':
    domain = input("Enter the domain name: ")
    result = execute("host", domain)
  elif dnscommand == 'd':
    domain = input("Enter the domain name: ")
    result = execute("dig", domain)
  elif dnscommand == 'e':
    print("Exiting")
    break
  elif dnscommand == "req":
    url = input("Please enter url for http request: ")
    result = http_request(url)
  elif dnscommand == "transfer":
    server = input("Enter server name: ")
    port = int(input("Enter port number: "))
    result = ftp_transfer(server, port)
  elif dnscommand == "protocol":
    task4()
  print(result)
