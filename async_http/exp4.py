"""Make 150 requests using aiohttp (collect return at the end)

How to control RPS
- First, set SLEEP_SECONDS to 0. And find a MAX_CONNECTOR that yields the maximum RPS
- Second, increase SLEEP_SECONDS to meet the desired RPS.

Note
- The response time measured in INACCURATE. To measure the response time, use 
  synchronus invocation (exp3.py)

"""

import aiohttp
import asyncio
import time

import numpy as np

# Constants
SLEEP_SECONDS = 0
MAX_CONNECTOR = 5

start_time = time.perf_counter()


async def get_pokemon(session, url):
    #tstart = time.perf_counter()
    tstart = asyncio.get_event_loop().time()
    async with session.get(url) as resp:
        # pokemon = await resp.json()
        # pokemon_name = pokemon['name']
        res = await resp.text()
        pokemon_name = "dummy"
        # await asyncio.sleep(0.1)
    #tused = time.perf_counter() - tstart
    tused = asyncio.get_event_loop().time() - tstart
    if SLEEP_SECONDS > 0:
        time.sleep(SLEEP_SECONDS)
        # asyncio.sleep(SLEEP_SECONDS)
    return pokemon_name, tused


async def main():

    connector = aiohttp.TCPConnector(limit=MAX_CONNECTOR)
    async with aiohttp.ClientSession(connector=connector) as session:

        tasks = []
        for number in range(1, 151):
            # url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            url = "https://google.com"
            # tasks.append(asyncio.ensure_future(get_pokemon(session, url)))
            tasks.append(asyncio.create_task(get_pokemon(session, url)))


        results = await asyncio.gather(*tasks)
        return results
        # for pokemon in original_pokemon:
        #     print(pokemon)

results = asyncio.run(main())

tused = time.perf_counter() - start_time

print(f"--- {tused} seconds ---")

print(f"With MAX_CONNECTOR = {MAX_CONNECTOR} and SLEEP_SECONDS = {SLEEP_SECONDS}, RPS = {len(results) / tused:.3f}")


total_times = np.array([res[1] for res in results])
quantiles = [0, 0.1, 0.5, 0.95, 0.99, 1]
quantiles_times = np.quantile(total_times, quantiles)
for quant, val in zip(quantiles, quantiles_times):
    print(f"{quant*100:.0f} quantile: {val*1000 :.2f} milliseconds")
