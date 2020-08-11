import socket
import threading
import pickle

from threading import Thread

from message import Messages
from socket_tools import SocketConsts

class InitSocket:
  HEADER = SocketConsts.HEADER
  PORT = SocketConsts.PORT
  FORMAT = SocketConsts.FORMAT

  SERVER = socket.gethostbyname(socket.gethostname())
  ADDR = (SERVER, PORT)

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(ADDR)

  clients = dict()

  '''
  This handles requests from the Client.
  '''
  def handle_client(self, conn, addr):
    '''
    This sends messages to the Client.
    It requires a Message as an input.
    (The messages do not have to be a string since it's pickled)
    IMPORTANT: 'conn' is a necessary input (See v0.2.0).
    '''
    def send(msg, conn):
      # This pickles the message so that non-string messages can also be sent.
      message = pickle.dumps(msg)

      # Creating and sending the fixed length header.
      conn.send(SocketConsts().fixed_length_header(message, self.FORMAT))

      # This is what sends the pickled message.
      conn.send(message)

    # New Client notification
    Messages().new_conn(addr)

    connected = True

    # Tells the Client how to disconnect.
    send(f"[INFO] Use '{Messages().DISCONNECT_MESSAGE}' to disconnect from the server!", conn)

    while connected:
      err = False

      try:
        # Getting the fixed length header from client.
        msg_length = conn.recv(self.HEADER).decode()

        if msg_length:
          msg_length = int(msg_length)
          msg = pickle.loads(conn.recv(msg_length))
          
          # Adds the Message to the 'clients' dictionary so it can be shown to all the other Clients.
          self.clients[addr] = msg

          # Checks to see if it is a disconnect message.
          if msg == Messages().DISCONNECT_MESSAGE:
            connected = False

      except:
        # Force disconnected Message.
        Messages().force_disconnect(addr)
        err = True

        # Closing connection.
        connected = False
        conn.close()
      
      # It displays different messages depending on whether the Client has asked to disconnect or not.
      if connected:
        Messages().display_msg(addr, msg)

        # Uses the 'clients' dictionary to find the last message sent by another the Clients.
        # The dictionary is looped through to get the last message from every Client.
        for client, msg in self.clients.items():
          # Every message appart from their own is sent to the Client.
          if client != addr:
            send(f"[{client}]: {msg}", conn)
      
      else:
        # Bug Patch that deletes a Clients message when they have disconnected.
        if addr in self.clients:
          del self.clients[addr]
        
    # If there are no errors when disconnecting.
    if err == False:
      send(Messages().disconnected_successfully_msg, conn)

      # Disconnects the Client and closes the connection.
      Messages().disconnected(addr)
      conn.close()

  def start(self):
    # Starting the server.
    server = self.server
    Messages().start()

    # Listening for requests.
    server.listen()
    Messages().listen(self.SERVER)

    while True:
      conn, addr = server.accept()
      
      # Starting new client thread.
      thread = Thread(target=self.handle_client, args=(conn, addr))
      thread.start()

      # Showing the number of active connections
      Messages().connections(threading.activeCount() - 1)

InitSocket().start()
