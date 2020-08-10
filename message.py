'''
This contains most of the messages and variables shared by the Client and Server.
'''
class Messages:
  DISCONNECT_MESSAGE = "!DISCONNECT"

  disconnected_successfully_msg = "Disconnected successfully."

  recieved = "Message recieved."

  def start(self):
    print("[STARTING] Running server...")
  
  def listen(self, SERVER):
    print(f"[LISTENING] Server is listening on {SERVER}")

  def connections(self, active):
    print(f"[ACTIVE CONNECTIONS] {active}")

  def new_conn(self, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

  def display_msg(self, addr, msg):
    print(f"[{addr}] {msg}")

  def disconnected(self, addr):
    print(f"[DISCONNECTED] {addr} disconnected successfully.")
  
  def force_disconnect(self, addr):
    print(f"[ERROR] {addr} closed unexpectedly.")