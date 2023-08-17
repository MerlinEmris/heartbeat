import asyncio
import json
import ssl
import socket
from urllib.parse import urlsplit
from typing import List, Dict

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


async def get_status(site: Dict[str,str]):
    """get status of site"""
    try:
        # split the url into components
        url_parsed = urlsplit(site['url'])

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
        return status, site

    except asyncio.TimeoutError:
        print("Connection timed out.")
    except ConnectionRefusedError:
        print("Connection refused.")
    except ssl.SSLError as ssl_err:
        print(f"SSL error: {ssl_err}")
    except socket.gaierror as dns_err:
        print(f"DNS resolution error: {dns_err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False, site

    

async def scanner(sites:List[Dict[str,str]], chanel_name) -> None:
    # create all coroutine requests
    channel_layer = get_channel_layer()
    await channel_layer.group_send(chanel_name, {"type": "state.info",
                                                      "data": {'type': 'success', 'message': 'Scan started!'}})
    coros = [get_status(url) for url in sites]
    # traverse tasks in completion order
    for coro in asyncio.as_completed(coros):
        # get status from task
        try:
            status, site = await coro

            # report status
            # TODO: send data to websocket
            # print(f'{url:30}:\t{status}')
            if status:
                status = status.split(' ')
                status = {'type': status[0],'code': status[1], 'message': ' '.join(status[2:])}
                await channel_layer.group_send(chanel_name, {"type": "scan.data",
                                                            "data": {'status': json.dumps(status), 'site': json.dumps(site)}})
            else:
                status = {'type': 'HTTP/1.1','code': 404, 'message': "Can not connect"}
                await channel_layer.group_send(chanel_name, {"type": "scan.data",
                                                            "data": {'status': json.dumps(status), 'site': json.dumps(site)}})
        except Exception as error:
            await channel_layer.group_send(chanel_name, {"type": "state.info",
                                                      "data": {'type': 'error', 'message': error}})

    await channel_layer.group_send(chanel_name, {"type": "state.info",
                                                          "data": {'type': 'success', 'message': 'Scan completed!'}})