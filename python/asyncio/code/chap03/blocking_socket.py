import socket

# setup what type of address our socket able to interact with, hostname and a port number
# setup to use TCP protocol.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allow us reuse port number after the stop and restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()  # listen for connection

connection, client_address = server_socket.accept()  # this method will block until we get a connection
print(f"I got a connection from {client_address}")  # "assign the client PO box")
      
