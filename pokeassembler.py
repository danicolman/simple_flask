import asyncio
import aiohttp
import json
from pprint import pprint

class Pokemon:
    def __init__(self, data):
        for key, val in data.items():
            if key in ["abilities", "cries", "forms", "height", "id", "name", "species", "types", "weight"]:
                self.__setattr__(key, val)

async def collect_pokemon_urls(session, url, url_list):
    async with session.get(url) as response:
        data = await response.json()
        
        for pokemon in data['results']:
            url_list.append(pokemon['url'])
        
        if data['next']:
            await collect_pokemon_urls(session, data['next'], url_list)

async def fetch_pokemon_data(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return Pokemon(data)

async def main():
    url_list = []
    master_list = []
    
    async with aiohttp.ClientSession() as session:

        await collect_pokemon_urls(session, 'https://pokeapi.co/api/v2/pokemon', url_list)
        
        tasks = [fetch_pokemon_data(session, url) for url in url_list]
        master_list = await asyncio.gather(*tasks)
    
    print(f"Collected {len(master_list)} Pokemon objects")
    return master_list

if __name__ == "__main__":
    pokemon_objects = asyncio.run(main())
    all_the_pokemon = [pokemon.__dict__ for pokemon in pokemon_objects]
    pprint(all_the_pokemon[0])
    with open("static/all_the_pokemon.json", "w") as max_pokemon:
        json.dump(all_the_pokemon, max_pokemon)