### Learning plan

- build a simple HTTP client
  - learn low level transport and protocol API
- stream reader and writer
  - build non-blocking SQL client
- use asyncio server API create client-server application.
  - Chat server and chat client

### Transports and protocols

Things to implement

- connection_made
- data_received
  - Buffer zone
- eof_received
  - end of file

Transports and protocols are very low level API, most of time we dont need to care about them.

High level API > `StreamReader` and `StreamWriter`

### StreamReader and StreamWriter

StreamWriter send HTTP request, StreamWriter read response.

StreamReader

- Readline coroutine, wait until we have one line of data
- read coroutine, wait until certain amount of bytes arrived.

StreamWriter

- write method, not a coroutine.
  - write to output buffer zone, if full, use queue
  - potential memory issue
- drain coroutine, block the data until all sent to socket

### Terminal raw mode cbreak mode and read coroutine

Cooked Mode: Canonical Mode

- line buffered, terminal collect input until Enter \n
- special char like Backspace, are handled by terminal driver
- program will only see the whole line **after** Enter

Raw Mode:

- no buffer, program see input immediately, char by char
- Enter doesn't do anything
- no process of any special char, Ctrl + C by default wont trigger SIGINT

Cbreak: Character-Break Mode

- input sent one char at a time.
- some processing like Ctrl+C is still active
- special char like backspace might not be working depending on settings

Need to reconsider the design under Cbreak mode

- readline wont work
- use read(1) to read single char and save to buffer

Requirements:

- user input should always at the bottom
- coroutine output should move from top of the screen
- when msg on screen more than available lines, move up current msg

Use deque! double ended queue

```
terminal:
-----------
|Message 1|
|Message 2|
|         |
|...      |
|delay: 1 | <- user input

```

- max number of elements in the deque is number of rows
- when a new msg appended to deque, move to the top of the screen and redraw each msg.

### Create a Server

- asyncio.start_server
- asyncio.client_connected_cb
  - callback func
  - or a coroutine that client will run when connected to server

Create another echo server

- echo user input
- show how many other clients are connected

### Chat Server and Chat Client

Server:

- client can connect to server once user name provided
- once connected user can send server msg, and each msg can send to all users
- idle 1min and disconnect user

Client:

- prompt to input user name, try to connect to server
- user can see other msg from top to bottom rolling
- bottom has input section, when hit Enter