# pyxivapi
An asynchronous Python client for XIVAPI

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/741f410aefad4fa69cc6925ff5d83b4b)](https://www.codacy.com/manual/Yandawl/xivapi-py?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xivapi/xivapi-py&amp;utm_campaign=Badge_Grade)
[![PyPI version](https://badge.fury.io/py/pyxivapi.svg)](https://badge.fury.io/py/pyxivapi)
[![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/)

## Requirements
```python
python>=3.6.0
asyncio
aiohttp
```

## Installation
```python
pip install pyxivapi
```

## Supported API end points

*   /character/search
*   /character/id
*   /freecompany/search
*   /freecompany/id
*   /linkshell/search
*   /linkshell/id
*   /pvpteam/search
*   /pvpteam/id
*   /index/search (e.g. recipe, item, action, pvpaction, mount, e.t.c.)
*   /index/id
*   /lore/search
*   /lodestone/worldstatus

## Documentation
<https://xivapi.com/docs/>

## Example
```python
import asyncio
import logging

import aiohttp
import pyxivapi
from pyxivapi.models import Filter, Sort


async def fetch_example_results():
    client = pyxivapi.XIVAPIClient(api_key="your_key_here")

    # Search Lodestone for a character
    character = await client.character_search(
        world="odin", 
        forename="lethys", 
        surname="lightpaw"
    )

    # Get a character by Lodestone ID with extended data & include their Free Company information, if it has been synced.
    character = await client.character_by_id(
        lodestone_id=8255311, 
        extended=True,
        include_freecompany=True
    )

    # Search Lodestone for a free company
    freecompany = await client.freecompany_search(
        world="gilgamesh", 
        name="Elysium"
    )

    # Item search with paging
    item = await client.index_search(
        name="Eden",
        indexes=["Item"],
        columns=["ID", "Name"],
        filters=[
            Filter("LevelItem", "gt", 520)
        ],
        sort=Sort("LevelItem", False),
        page=0,
        per_page=10
    )

    # Fuzzy search XIVAPI game data for a recipe by name. Results will be in English.
    recipe = await client.index_search(
        name="Crimson Cider", 
        indexes=["Recipe"], 
        columns=["ID", "Name", "Icon", "ItemResult.Description"]
    )

    # Fuzzy search XIVAPI game data for a recipe by name. Results will be in French.
    recipe = await client.index_search(
        name="Cidre carmin", 
        indexes=["Recipe"], 
        columns=["ID", "Name", "Icon", "ItemResult.Description"], 
        language="fr"
    )

    # Get an item by its ID (Omega Rod) and return the data in German
    item = await client.index_by_id(
        index="Item", 
        content_id=23575, 
        columns=["ID", "Name", "Icon", "ItemUICategory.Name"], 
        language="de"
    )

    filters = [
        Filter("ClassJobLevel", "gte", 0)
    ]

    # Get non-npc actions matching a given term (Defiance)
    action = await client.index_search(
        name="Defiance", 
        indexes=["Action", "PvPAction", "CraftAction"], 
        columns=["ID", "Name", "Icon", "Description", "ClassJobCategory.Name", "ClassJobLevel", "ActionCategory.Name"], 
        filters=filters,
        string_algo="match"
    )

    # Search ingame data for matches against a given query. Includes item, minion, mount & achievement descriptions, quest dialog & more.
    lore = await client.lore_search(
        query="Shiva",
        language="fr"
    )

    # Search for an item using specific filters
    filters = [
        Filter("LevelItem", "gte", 100)
    ]

    sort = Sort("LevelItem", True)

    item = await client.index_search(
        name="Omega Rod", 
        indexes=["Item"], 
        columns=["ID", "Name", "Icon", "Description", "LevelItem"],
        filters=filters,
        sort=sort,
        language="de"
    )

    await client.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_example_results())

```
