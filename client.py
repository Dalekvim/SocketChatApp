import socket
import pickle

from socket_tools import SocketConsts
from message import Messages

from threading import Thread
from time import sleep

class Client:
  HEADER = SocketConsts.HEADER
  PORT = SocketConsts.PORT
  FORMAT = SocketConsts.FORMAT

  # This can be changed to the IP of the Server you want to connect to.
  SERVER = socket.gethostbyname(socket.gethostname()) # E.g. '192.168.56.1'
  ADDR = (SERVER, PORT)

  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(ADDR)

  '''
  This sends messages to the Server.
  It requires a Message as an input.
  (The messages do not have to be a string since it's pickled)
  '''
  def send(self, msg):
    FORMAT = self.FORMAT
    client = self.client

    message = pickle.dumps(msg)

    client.send(SocketConsts().fixed_length_header(message, FORMAT))
    client.send(message)

  '''
  This recieves messages from the Server.
  It requires a Socket as input.
  '''
  def recv(self, client):
    while True:
      msg_length = client.recv(self.HEADER).decode()
      if msg_length:
        msg_length = int(msg_length)

        # This unpickles the content so that it can be displayed.
        msg = pickle.loads(client.recv(msg_length))
        
        # Checks if it is a disconnect message.
        if msg == Messages.disconnected_successfully_msg:
          break

        print(msg)

def connect_client():
  print(f"[CONNECTION] Connecting to {Client.ADDR}")

  # New thread recieves messages from the server.
  thread = Thread(target=Client.recv, args=(Client, Client.client))
  thread.start()

  print("[CONNECTED] Enter a message below.")
  while True:
    msg = input()

    if msg == Messages.DISCONNECT_MESSAGE:
      print("[DISCONNECT] Disconnecting...")
      sleep(3)
      Client().send(msg)
      break

    Client().send(msg)

connect_client()