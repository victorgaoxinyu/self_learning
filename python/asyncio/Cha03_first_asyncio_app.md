### Goal
- Create a server that can handle multi users' request, using one thread.

### Blocking Sockets

```
 Client side                             Server side
 --------                              ---------------
| Client |  -- request to connect --> | Server Socket |
 --------                              ---------------
    A                                        |
    |                                        | establish client socket
    |                                        V
    |      read and write              ---------------
    --------------------------------> | Client socket |
                                       ---------------
```
When more than one client connected, one client could cause others to wait for it to send data.


### Non-blocking socket
- set both client and server to use non-blocking.
- this will increase cpu usage as it will keep iter and catch exceptions.

### Use selector
- provide OS a list of sockets we want to monitor for events, instead of constantly checking each socket.
- abstract base class `BaseSelector`
  - `registration`: register the socket we care with selector, and tell it which wevents we cares
  - `select`: block until an event has happened, and then return a list of sockets that ready for processing

### Use asyncio event loop
- `sock_accept`, `sock_recv` and `sock_sendall`

```python

# connection, address = server_socket.accept()
connection, address = await loop.sock_accept(socket)

# data = event_socket.recv(1024)
data = await loop.sock_recv(socket)

# event_socket.send(data)
success = await loop.sock_sendall(socket, data)
```
