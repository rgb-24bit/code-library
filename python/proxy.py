#!/usr/bin/env python3

"""
proxy.py - A simple tcp proxy(Python3.5+).
"""

import argparse
import asyncio


async def copy_one_direction(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        writer.write(data)
        await writer.drain()
    writer.close()


def main(local_addr: str, remote_addr: str):
    local_host, local_port = local_addr.split(':')
    remote_host, remote_port = remote_addr.split(':')

    async def handle_accept(reader, writer):
        print('connection from', writer.get_extra_info('peername'))

        remote_reader, remote_writer = await asyncio.open_connection(
            remote_host, remote_port)

        asyncio.ensure_future(copy_one_direction(reader, remote_writer))
        asyncio.ensure_future(copy_one_direction(remote_reader, writer))

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_accept, local_host, local_port, loop=loop)
    server = loop.run_until_complete(coro)

    print('serving on {}'.format(server.sockets[0].getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='a simple tcp proxy.')

    parser.add_argument('-l', '--local', type=str, required=True, help='local ip:port')
    parser.add_argument('-r', '--remote', type=str, required=True, help='remote ip:port')

    args = parser.parse_args()

    main(args.port, args.remote)
