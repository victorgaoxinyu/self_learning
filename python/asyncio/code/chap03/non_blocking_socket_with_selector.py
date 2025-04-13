import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.setblocking(False)  # set server side socket non-blocking
server_socket.bind(server_address)
server_socket.listen()  # listen for connection

# 注册服务器socket到选择器
# 通知选择器监控可读事件，当有新客户端链接的时候，sever_socket变为可读
# 选择器通知程序
selector.register(server_socket, selectors.EVENT_READ)

while True:
    # 如果有事件发生，select()会返回tuple列表
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        # print("No events, waiting a bit more")
        pass
    
    for event, _ in events:
        event_socket = event.fileobj

        if event_socket == server_socket:
            connection, address = server_socket.accept()  # nonblocking
            connection.setblocking(False)
            print(f"I got a connection from {address}")
            print(f"Event Socket is: {event_socket}")
            # Event Socket is:
            # <socket.socket fd=4, family=AddressFamily.AF_INET,
            # type=SocketKind.SOCK_STREAM, proto=0,
            # laddr=('127.0.0.1', 8000)>
            # 只有本地地址laddr，没有远程日志raddr
            # 因为不直接与客户端通信，负责接收新链接

            # 注册客户端socket到选择器
            selector.register(connection, selectors.EVENT_READ)
        else:
            print(f"Event Socket is: {event_socket}")
            # Event Socket is: 
            # <socket.socket fd=5, family=AddressFamily.AF_INET,
            # type=SocketKind.SOCK_STREAM, proto=0,
            # laddr=('127.0.0.1', 8000), raddr=('127.0.0.1', 57217)>
            # 负责与特定客户通信
            
            # 客户端可读事件，说明有数据到达
            data = event_socket.recv(1024)
            print(f"I got some data: {data}")
            event_socket.send(data)


