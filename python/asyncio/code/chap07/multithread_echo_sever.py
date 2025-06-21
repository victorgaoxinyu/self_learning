from threading import Thread
import socket

def echo(client: socket):
    while True:
        data = client.recv(2048)
        print(f"Received {data}, sending!")
        client.sendall(data)
    
def run_normal_echo_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 8000))
        server.listen()
        while True:
            connection, _ = server.accept()
            thread = Thread(target=echo, args=(connection,))
            thread.daemon = True  # this will create daemon thread
            print(f"Connection: {connection}, thread: {thread}")
            thread.start()


class ClientEchoThread(Thread):
    
    def __init__(self, client):
        super().__init__()
        self.client = client
    
    def run(self):
        try:
            while True:
                data = self.client.recv(2048)
                if not data:
                    # when client is closed, this might happen
                    raise BrokenPipeError("Connection close!")
                
                print(f"Received {data}, sending!")
                self.client.sendall(data)
        except OSError as e:
            print(f"Thread interrupted by {e} exception, shutting down!")
    
    def close(self):
        if self.is_alive():
            self.client.sendall(bytes('Shutting down!!!!', encoding="utf-8"))
            self.client.shutdown(socket.SHUT_RDWR)

def run_echo_server_with_custom_thread_cls():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 8000))
        server.listen()
        connection_threads = []
        try:
            while True:
                connection, _ = server.accept()
                thread = ClientEchoThread(connection)
                connection_threads.append(thread)
                print(f"Connection: {connection}, thread: {thread}")
                thread.start()
        except KeyboardInterrupt:
            print("Shutting down!\n")
            [thread.close() for thread in connection_threads]


if __name__ == "__main__":
    # run_normal_echo_server()
    run_echo_server_with_custom_thread_cls()