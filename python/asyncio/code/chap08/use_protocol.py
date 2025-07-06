import asyncio
from asyncio import AbstractEventLoop
from HttpGetClientProtocol import HTTPGetClietnProtocol

async def make_request(host: str, port: int, loop: AbstractEventLoop) -> str:
    def protocol_factory():
        return HTTPGetClietnProtocol(host, loop)
    
    _, protocol = await loop.create_connection(protocol_factory, host=host, port=port)
    return await protocol.get_response()

async def main():
    loop = asyncio.get_running_loop()
    result = await make_request('www.example.com', 80, loop)
    print(result)


asyncio.run(main())
