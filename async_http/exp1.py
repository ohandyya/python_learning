"""Make a single request using aiohttp3"""
import aiohttp
import asyncio


async def main():

    async with aiohttp.ClientSession() as session:
        # By default, each session can make connection up to 100 different servers at a time.

        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            # import pdb; pdb.set_trace()
            print(pokemon['name'])

asyncio.run(main())
