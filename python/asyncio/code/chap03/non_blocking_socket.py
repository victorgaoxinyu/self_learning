import socket

# setup what type of address our socket able to interact with, hostname and a port number
# setup to use TCP protocol.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allow us reuse port number after the stop and restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()  # listen for connection

server_socket.setblocking(False)  # set server side socket non-blocking

connections = []

try:
    while True:
        try:
            connection, client_address = server_socket.accept()  # this method will block until we get a connection
            print(f"I got a connection from {client_address}")  # "assign the client PO box")
            connection.setblocking(False)  # set client side socket non-blocking
            connections.append(connection)
        except BlockingIOError:
            pass  # 继续循环直到得到数据

        for connection in connections:
            try:
                buffer = b''
                # connection.send(b"Type anything!\r\n")

                while buffer[-2:] != b'\r\n':
                    data = connection.recv(2)  # receive from client
                    if not data:
                        break
                    else:
                        print(f"I got data: {data}!")
                        buffer = buffer + data
                # print(f"All the data is: {buffer}")
                # connection.send(f"You have just typed: \n{buffer}\r\n".encode())  # send back to client
            except BlockingIOError:
                pass

finally:
    server_socket.close()
