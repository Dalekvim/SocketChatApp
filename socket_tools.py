class SocketConsts:
  HEADER = 64
  PORT = 5050
  FORMAT = 'utf-8'
  
  def fixed_length_header(self, message, FORMAT):
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (self.HEADER - len(send_length))
    return send_length
