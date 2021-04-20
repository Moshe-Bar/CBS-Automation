import asyncio
import json
import time

import aiohttp

from writeToFile import readFile


async def testLinks(session, link, i):
    async with session.get(link) as response:
        print(str(response[0]) + ' ' + str(i))

    # with session.get(link) as response:
    #     print(link + ': ' + response.status_code)
    #     u_list.append((link, response.status_code))

    # try:
    #     r = requests.head(link[0])
    # except Exception as e:
    #     print(e.__cause__)
    # if not r.status_code == 200:
    #     print('not 200')
    # print(link[1], r.status_code)


async def main():
    start_time = time.time()
    sessions = []
    try:
        l_list = readFile()
        sessions = [aiohttp.ClientSession() for i in range(20)]
        async with aiohttp.ClientSession() as session:
            tasks = [testLinks(sessions[i % 20], l_list[i], i) for i in range(len(l_list))]
            await asyncio.gather(*tasks)
            for i in sessions:
                await session.close()
            print(time.time() - start_time)
    except Exception as e:
        print(e.__cause__)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
