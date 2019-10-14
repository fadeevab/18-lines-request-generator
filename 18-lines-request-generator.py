#!/usr/bin/env python3.7

import aiohttp
import asyncio

MAXREQ = 500
MAXTHREAD = 50
URL = 'https://google.com'

g_thread_limit = asyncio.Semaphore(MAXTHREAD)


async def worker(session):
    async with session.get(URL) as response:
        await response.read()


async def run(worker, *argv):
    async with g_thread_limit:
        await worker(*argv)


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[run(worker, session) for _ in range(MAXREQ)])


if __name__ == '__main__':
    # Don't use asyncio.run() - it produces a lot of errors on exit.
    asyncio.get_event_loop().run_until_complete(main())
