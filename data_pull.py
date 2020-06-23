"""Super Hero API - Data Pull

This script will scrape Super Hero IDs from the
Super Hero API webpage, and then continue to
ingest all the Super Hero data from the API. Data
is persisted on a Heroku Postgres instance.

Args:
    API_TOKEN: Super Hero API access token

"""

from db_model import SuperHeros, PowerStats, Biography, Aliases, Appearance
from db_model import session, Work, Connections, Image
from typing import Union, List, Dict
from bs4 import BeautifulSoup
import requests
import os

# Envionrment Variables
API_TOKEN=os.getenv('API_TOKEN', None)

assert(not API_TOKEN is None)

# Scraping
def get_super_hero_ids() -> List[Dict]:
    """Pull Super Hero IDs

    Scrape the Super Hero API website for IDs.

    ..note:
        No endpoint exists to pull super hero IDs
        from API calls.

    Returns:
        List of super hero IDs & names
    
    Raises:
        Exception: Error occuring normally from API connection
    """
    try:
        headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.5',
            'connection': 'keep-alive',
            'DNT': '1',
            'host': 'superheroapi.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        source = requests.get('https://superheroapi.com/ids.html', headers=headers)
        source = BeautifulSoup(source.text, 'html.parser')
        tables = source.select('.container-fluid table')
        ids = []
        
        for t in tables:
            rows = t.select('tbody tr')
            
            for r in rows:
                elem = r.find_all('td')
                ids.append({
                    'id': elem[0].text,
                    'name': elem[1].text
                })
        
        return ids
    except Exception:
        raise Exception('Can\'t Connect to Super Hero API ID Table')


def write_super_hero_ids(ids: List[Dict]):
    """Write Super Hero IDs to SQL

    Args:
        ids: List of super hero IDs and names
    """
    super_heros = [SuperHeros(id=i['id'], name=i['name']) for i in ids]
    session.add_all(super_heros)
    session.commit()


# API
def _clean(sp_dict: Union[Dict, List, str]):
    """Clean Super Hero API JSON Responses

    Recursively clean null values to the python None equivalent

    Args:
        sp_dict: Super hero JSON response
    
    Returns:
        Clean response for parsing
    
    Raises:
        Exception: Recursive catch for lists or values
    """
    try:
        clean_dict = {}
        for k, v in sp_dict.items():
            if isinstance(v, dict):
                clean_dict[k] = _clean(v)
            elif isinstance(v, list):
                clean_dict[k] = [_clean(i) for i in v]
            elif v == 'null':
                clean_dict[k] = None
            else:
                clean_dict[k] = v
        
        return clean_dict
    except Exception:
        if sp_dict == 'null':
            return None
        
        return sp_dict

def get_super_hero(id: Union[str,int]) -> Dict:
    """Get Super Hero

    Pull Super Hero from API.

    Args:
        id: Super hero ID
    
    Returns:
        Super hero data dictionary
    """
    response = requests.get('https://superheroapi.com/api/%s/%s' % (API_TOKEN, str(id)))
    sp_dict = response.json()
    return _clean(sp_dict)

def write_powerstats(hero: Dict):
    """Write Super Hero Powerstats to SQL

    Args:
        hero: Super hero data dictionary
    """
    powerstats = PowerStats(
        id=hero['id'],
        intelligence=hero['powerstats']['intelligence'],
        strength=hero['powerstats']['strength'],
        speed=hero['powerstats']['speed'],
        durability=hero['powerstats']['durability'],
        power=hero['powerstats']['power'],
        combat=hero['powerstats']['combat'])
    session.add(powerstats)
    session.commit()

def write_biography(hero: Dict):
    """Write Super Hero Biography to SQL

    Args:
        hero: Super hero data dictionary
    """
    biography = Biography(
        id=hero['id'],
        full_name=hero['biography']['full-name'],
        alter_egos=hero['biography']['alter-egos'],
        place_of_birth=hero['biography']['place-of-birth'],
        first_appearance=hero['biography']['first-appearance'],
        publisher=hero['biography']['publisher'],
        alignment=hero['biography']['alignment'])
    session.add(biography)
    session.commit()

def write_aliases(hero: Dict):
    """Write Super Hero Aliases to SQL

    Args:
        hero: Super hero data dictionary
    """
    for i,a in enumerate(hero['biography']['aliases']):
        alias = Aliases(
            id=hero['id'],
            alias_id=i,
            name=a)
        session.add(alias)
        session.commit()

def write_appearance(hero: Dict):
    """Write Super Hero Appearnace to SQL

    Args:
        hero: Super hero data dictionary
    """
    if len(hero['appearance']['height']) < 2:
        hero['appearance']['height'] = [None, None]

    appearance = Appearance(
        id=hero['id'],
        gender=hero['appearance']['gender'],
        race=hero['appearance']['race'],
        height_imperial=hero['appearance']['height'][0],
        height_metric=hero['appearance']['height'][1],
        weight_imperial=hero['appearance']['weight'][0],
        weight_metric=hero['appearance']['weight'][1],
        eye_colour=hero['appearance']['eye-color'],
        hair_colour=hero['appearance']['hair-color'])
    session.add(appearance)
    session.commit()

def write_work(hero: Dict):
    """Write Super Hero Work to SQL

    Args:
        hero: Super hero data dictionary
    """
    work = Work(
        id=hero['id'],
        occupation=hero['work']['occupation'],
        base=hero['work']['base'])
    session.add(work)
    session.commit()

def write_connections(hero: Dict):
    """Write Super Hero Connections to SQL

    Args:
        hero: Super hero data dictionary
    """
    connections = Connections(
        id=hero['id'],
        group_affiliation=hero['connections']['group-affiliation'],
        relatives=hero['connections']['relatives'])
    session.add(connections)
    session.commit()

def write_image(hero: Dict):
    """Write Super Hero Image to SQL

    Args:
        hero: Super hero data dictionary
    """
    image = Image(
        id=hero['id'],
        url=hero['image']['url'])
    session.add(image)
    session.commit()



# Run
def main():
    """Super Hero Data Ingestion

    Scrape and pull all super heros from the Super Hero API
    website and API. Store the results in the SQL database
    with the connections created in db_model script.
    """
    print('Pulling Super Hero IDs')
    ids = get_super_hero_ids()
    write_super_hero_ids(ids)
    
    for hero_meta in session.query(SuperHeros):
        print('Pulling Super Hero: %s' % hero_meta.name)
        hero = get_super_hero(hero_meta.id)
        if hero['response'] == 'success':
            write_powerstats(hero)
            write_biography(hero)
            write_aliases(hero)
            write_appearance(hero)
            write_work(hero)
            write_connections(hero)
            write_image(hero)

if __name__ == '__main__':
    main()
