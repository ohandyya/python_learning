"""Make 150 requests using aiohttp

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
from typing import Tuple

import numpy as np

# Constants
SLEEP_SECONDS = 0
MAX_CONNECTOR = 100


start_time = time.perf_counter()


async def get_pokemon(session: aiohttp.ClientSession, number: int) -> Tuple[float, str]:
    #tstart= asyncio.get_event_loop().time()
    tstart = time.perf_counter()
    #pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'
    pokemon_url = "https://google.com"
    async with session.get(pokemon_url) as resp:
        resp.raise_for_status()
        res = await resp.text()
        pokemon_name = "dummy"
        #pokemon = await resp.json()
        #pokemon_name = pokemon["name"]
    
    # tused = asyncio.get_event_loop().time() - tstart
    tused = time.perf_counter() - tstart

    return pokemon_name, tused


async def main():

    result_names = {}
    total_times = []

    connector = aiohttp.TCPConnector(limit=MAX_CONNECTOR)
    async with aiohttp.ClientSession(connector=connector) as session:

        for number in range(1, 151):
            pokemon_name, tused = await get_pokemon(session, number)
            result_names[number] = pokemon_name
            total_times.append(tused)
            if SLEEP_SECONDS > 0:
                time.sleep(SLEEP_SECONDS)

    return result_names, total_times

result_names, total_times = asyncio.run(main())

tused = time.perf_counter() - start_time

print(f"--- {tused} seconds ---")

print(f"With MAX_CONNECTOR = {MAX_CONNECTOR} and SLEEP_SECONDS = {SLEEP_SECONDS}, RPS = {len(result_names) / tused:.3f}")

total_times = np.array(total_times)
quantiles = [0, 0.1, 0.5, 0.95, 0.99, 1]
quantiles_times = np.quantile(total_times, quantiles)
for quant, val in zip(quantiles, quantiles_times):
    print(f"{quant*100:.0f} quantile: {val*1000 :.2f} milliseconds")
