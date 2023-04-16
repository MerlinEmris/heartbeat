import asyncio
from urllib.parse import urlsplit
from typing import List

async def get_status(url: str):
    """get status of site"""
    # split the url into components
    url_parsed = urlsplit(url)
    # open the connection
    if url_parsed.scheme == 'https':
        reader, writer = await asyncio.open_connection(url_parsed.hostname, 443, ssl=True)
    else:
        reader, writer = await asyncio.open_connection(url_parsed.hostname, 80)
    # send GET request
    query = f'GET {url_parsed.path} HTTP/1.1\r\nHost: {url_parsed.hostname}\r\n\r\n'
    # write query to socket
    writer.write(query.encode())
    # wait for the bytes to be written to the socket
    await writer.drain()
    # read the single line response
    response = await reader.readline()
    # close the connection
    writer.close()
    # decode and strip white space
    status = response.decode().strip()
    # return the response
    return status

async def scanner(sites: List[str]) -> None:
    # create all coroutine requests
    coros = [get_status(url) for url in sites]
    # traverse tasks in completion order
    for coro in asyncio.as_completed(coros):
        # get status from task
        status, url = await coro
        # report status
        # TODO: send data to websocket
        print(f'{url:30}:\t{status}')