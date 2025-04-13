import asyncio
import socket
import logging
from asyncio import AbstractEventLoop


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    # 无限循环等待来自客户端的数据
    try:
        while data := await loop.sock_recv(connection, 1024):
            if data == b'boom\r\n':
                raise Exception("Unexcepted network error")
            # 一旦得到数据，发送回客户端
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


# 无限循环并监听任何传入连接
async def listen_for_connections(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        # 每当获得连接的时候，创建一个echo任务来监听客户端数据
        asyncio.create_task(echo(connection, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listen_for_connections(server_socket, asyncio.get_event_loop())

asyncio.run(main())