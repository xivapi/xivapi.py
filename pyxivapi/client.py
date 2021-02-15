import logging
from typing import List, Optional

from aiohttp import ClientSession

from .exceptions import (
    XIVAPIBadRequest, XIVAPIForbidden, XIVAPINotFound, XIVAPIServiceUnavailable, 
    XIVAPIInvalidLanguage, XIVAPIError, XIVAPIInvalidIndex, XIVAPIInvalidColumns, 
    XIVAPIInvalidAlgo
)
from .decorators import timed
from .models import Filter, Sort

__log__ = logging.getLogger(__name__)


class XIVAPIClient:
    """
    Asynchronous client for accessing XIVAPI's endpoints.
    Parameters
    ------------
    api_key: str
        The API key used for identifying your application with XIVAPI.com.
    session: Optional[ClientSession]
        Optionally include your aiohttp session
    """
    base_url = "https://xivapi.com"
    languages = ["en", "fr", "de", "ja"]

    def __init__(self, api_key: str, session: Optional[ClientSession] = None) -> None:
        self.api_key = api_key
        self._session = session

        self.base_url = "https://xivapi.com"
        self.languages = ["en", "fr", "de", "ja"]
        self.string_algos = [
            "custom", "wildcard", "wildcard_plus", "fuzzy", "term", "prefix", "match", "match_phrase",
            "match_phrase_prefix", "multi_match", "query_string"
        ]

    @property
    def session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession()
        return self._session

    @timed
    async def character_search(self, world, forename, surname, page=1):
        """|coro|
        Search for character data directly from the Lodestone.
        Parameters
        ------------
        world: str
            The world that the character is attributed to.
        forename: str
            The character's forename.
        surname: str
            The character's surname.
        Optional[page: int]
            The page of results to return. Defaults to 1.
        """
        url = f'{self.base_url}/character/search?name={forename}%20{surname}&server={world}&page={page}&private_key={self.api_key}'
        async with self.session.get(url) as response:
            return await self.process_response(response)

    @timed
    async def character_by_id(self, lodestone_id: int, extended=False, include_achievements=False, include_minions_mounts=False, include_classjobs=False, include_friendslist=False, include_freecompany=False, include_freecompany_members=False, include_pvpteam=False, language="en"):
        """|coro|
        Request character data from XIVAPI.com
        Please see XIVAPI documentation for more information about character sync state https://xivapi.com/docs/Character#character
        Parameters
        ------------
        lodestone_id: int
            The character's Lodestone ID.
        """

        params = {
            "private_key": self.api_key,
            "language": language
        }

        if language.lower() not in self.languages:
            raise XIVAPIInvalidLanguage(f'"{language}" is not a valid language code for XIVAPI.')

        if extended is True:
            params["extended"] = 1

        data = []
        if include_achievements is True:
            data.append("AC")

        if include_minions_mounts is True:
            data.append("MIMO")

        if include_friendslist is True:
            data.append("FR")

        if include_classjobs is True:
            data.append("CJ")

        if include_freecompany is True:
            data.append("FC")

        if include_freecompany_members is True:
            data.append("FCM")

        if include_pvpteam is True:
            data.append("PVP")

        if len(data) > 0:
            params["data"] = ",".join(data)

        url = f'{self.base_url}/character/{lodestone_id}'
        async with self.session.get(url, params=params) as response:
            return await self.process_response(response)

    @timed
    async def freecompany_search(self, world, name, page=1):
        """|coro|
        Search for Free Company data directly from the Lodestone.
        Parameters
        ------------
        world: str
            The world that the Free Company is attributed to.
        name: str
            The Free Company's name.
        Optional[page: int]
            The page of results to return. Defaults to 1.
        """
        url = f'{self.base_url}/freecompany/search?name={name}&server={world}&page={page}&private_key={self.api_key}'
        async with self.session.get(url) as response:
            return await self.process_response(response)

    @timed
    async def freecompany_by_id(self, lodestone_id: int, extended=False, include_freecompany_members=False):
        """|coro|
        Request Free Company data from XIVAPI.com by Lodestone ID
        Please see XIVAPI documentation for more information about Free Company info at https://xivapi.com/docs/Free-Company#profile
        Parameters
        ------------
        lodestone_id: int
            The Free Company's Lodestone ID.
        """

        params = {
            "private_key": self.api_key
        }

        if extended is True:
            params["extended"] = 1

        data = []
        if include_freecompany_members is True:
            data.append("FCM")

        if len(data) > 0:
            params["data"] = ",".join(data)

        url = f'{self.base_url}/freecompany/{lodestone_id}'
        async with self.session.get(url, params=params) as response:
            return await self.process_response(response)

    @timed
    async def linkshell_search(self, world, name, page=1):
        """|coro|
        Search for Linkshell data directly from the Lodestone.
        Parameters
        ------------
        world: str
            The world that the Linkshell is attributed to.
        name: str
            The Linkshell's name.
        Optional[page: int]
            The page of results to return. Defaults to 1.
        """
        url = f'{self.base_url}/linkshell/search?name={name}&server={world}&page={page}&private_key={self.api_key}'
        async with self.session.get(url) as response:
            return await self.process_response(response)

    @timed
    async def linkshell_by_id(self, lodestone_id: int):
        """|coro|
        Request Linkshell data from XIVAPI.com by Lodestone ID
        Parameters
        ------------
        lodestone_id: int
            The Linkshell's Lodestone ID.
        """
        url = f'{self.base_url}/linkshell/{lodestone_id}?private_key={self.api_key}'
        async with self.session.get(url) as response:
            return await self.process_response(response)

    @timed
    async def pvpteam_search(self, world, name, page=1):
        """|coro|
        Search for PvPTeam data directly from the Lodestone.
        Parameters
        ------------
        world: str
            The world that the PvPTeam is attributed to.
        name: str
            The PvPTeam's name.
        Optional[page: int]
            The page of results to return. Defaults to 1.
        """
        url = f'{self.base_url}/pvpteam/search?name={name}&server={world}&page={page}&private_key={self.api_key}'
        async with self.session.get(url) as response:
            return await self.process_response(response)

    @timed
    async def pvpteam_by_id(self, lodestone_id):
        """|coro|
        Request PvPTeam data from XIVAPI.com by Lodestone ID
        Parameters
        ------------
        lodestone_id: str
            The PvPTeam's Lodestone ID.
        """
        url = f'{self.base_url}/pvpteam/{lodestone_id}?private_key={self.api_key}'
        async with self.session.get(url) as response:
            return await self.process_response(response)

    @timed
    async def index_search(self, name, indexes=(), columns=(), filters: List[Filter] = (), sort: Sort = None, page=0, per_page=10, language="en", string_algo="match"):
        """|coro|
        Search for data from on specific indexes.
        Parameters
        ------------
        name: str
            The name of the item to retrieve the recipe data for.
        indexes: list
            A named list of indexes to search XIVAPI. At least one must be specified.
            e.g. ["Recipe", "Item"]
        Optional[columns: list]
            A named list of columns to return in the response. ID, Name, Icon & ItemDescription will be returned by default.
            e.g. ["ID", "Name", "Icon"]
        Optional[filters: list]
            A list of type Filter. Filter must be initialised with Field, Comparison (e.g. lt, lte, gt, gte) and value.
            e.g. filters = [ Filter("LevelItem", "gte", 100) ]
        Optional[sort: Sort]
            The name of the column to sort on.
        Optional[page: int]
            The page of results to return. Defaults to 1.
        Optional[language: str]
            The two character length language code that indicates the language to return the response in. Defaults to English (en).
            Valid values are "en", "fr", "de" & "ja"
        Optional[string_algo: str]
            The search algorithm to use for string matching (default = "match")
            Valid values are "custom", "wildcard", "wildcard_plus", "fuzzy", "term", "prefix", "match", "match_phrase",
            "match_phrase_prefix", "multi_match", "query_string"
        """

        if len(indexes) == 0:
            raise XIVAPIInvalidIndex("Please specify at least one index to search for, e.g. [\"Recipe\"]")

        if language.lower() not in self.languages:
            raise XIVAPIInvalidLanguage(f'"{language}" is not a valid language code for XIVAPI.')

        if len(columns) == 0:
            raise XIVAPIInvalidColumns("Please specify at least one column to return in the resulting data.")

        if string_algo not in self.string_algos:
            raise XIVAPIInvalidAlgo(f'"{string_algo}" is not a supported string_algo for XIVAPI')

        body = {
            "indexes": ",".join(list(set(indexes))),
            "columns": "ID",
            "body": {
                "query": {
                    "bool": {
                        "should": [{
                            string_algo: {
                                "NameCombined_en": {
                                    "query": name,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 1,
                                    "max_expansions": 50
                                }
                            }
                        }, {
                            string_algo: {
                                "NameCombined_de": {
                                    "query": name,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 1,
                                    "max_expansions": 50
                                }
                            }
                        }, {
                            string_algo: {
                                "NameCombined_fr": {
                                    "query": name,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 1,
                                    "max_expansions": 50
                                }
                            }
                        }, {
                            string_algo: {
                                "NameCombined_ja": {
                                    "query": name,
                                    "fuzziness": "AUTO",
                                    "prefix_length": 1,
                                    "max_expansions": 50
                                }
                            }
                        }]
                    }
                },
                "from": page,
                "size": per_page
            }
        }

        if len(columns) > 0:
            body["columns"] = ",".join(list(set(columns)))

        if len(filters) > 0:
            filts = []
            for f in filters:
                filts.append({
                    "range": {
                        f.Field: {
                            f.Comparison: f.Value
                        }
                    }
                })

            body["body"]["query"]["bool"]["filter"] = filts

        if sort:
            body["body"]["sort"] = [{
                sort.Field: "asc" if sort.Ascending else "desc"
            }]

        url = f'{self.base_url}/search?language={language}&private_key={self.api_key}'
        async with self.session.post(url, json=body) as response:
            return await self.process_response(response)

    @timed
    async def index_by_id(self, index, content_id: int, columns=(), language="en"):
        """|coro|
        Request data from a given index by ID.
        Parameters
        ------------
        index: str
            The index to which the content is attributed.
        content_id: int
            The ID of the content
        Optional[columns: list]
            A named list of columns to return in the response. ID, Name, Icon & ItemDescription will be returned by default.
            e.g. ["ID", "Name", "Icon"]
        Optional[language: str]
            The two character length language code that indicates the language to return the response in. Defaults to English (en).
            Valid values are "en", "fr", "de" & "ja"
        """
        if index == "":
            raise XIVAPIInvalidIndex("Please specify an index to search on, e.g. \"Item\"")

        if len(columns) == 0:
            raise XIVAPIInvalidColumns("Please specify at least one column to return in the resulting data.")

        params = {
            "private_key": self.api_key,
            "language": language
        }

        if len(columns) > 0:
            params["columns"] = ",".join(list(set(columns)))

        url = f'{self.base_url}/{index}/{content_id}'
        async with self.session.get(url, params=params) as response:
            return await self.process_response(response)

    @timed
    async def lore_search(self, query, language="en"):
        """|coro|
        Search cutscene subtitles, quest dialog, item, achievement, mount & minion descriptions and more for any text that matches query.
        Parameters
        ------------
        query: str
            The text to search game content for.
        Optional[language: str]
            The two character length language code that indicates the language to return the response in. Defaults to English (en).
            Valid values are "en", "fr", "de" & "ja"
        """
        params = {
            "private_key": self.api_key,
            "language": language,
            "string": query
        }

        url = f'{self.base_url}/lore'
        async with self.session.get(url, params=params) as response:
            return await self.process_response(response)

    @timed
    async def lodestone_worldstatus(self):
        """|coro|
        Request world status post from the Lodestone.
        """
        url = f'{self.base_url}/lodestone/worldstatus?private_key={self.api_key}'
        async with self.session.get(url) as response:
            return await self.process_response(response)

    async def process_response(self, response):
        __log__.info(f'{response.status} from {response.url}')

        if response.status == 200:
            return await response.json()

        if response.status == 400:
            raise XIVAPIBadRequest("Request was bad. Please check your parameters.")

        if response.status == 401:
            raise XIVAPIForbidden("Request was refused. Possibly due to an invalid API key.")

        if response.status == 404:
            raise XIVAPINotFound("Resource not found.")

        if response.status == 500:
            raise XIVAPIError("An internal server error has occured on XIVAPI.")

        if response.status == 503:
            raise XIVAPIServiceUnavailable("Service is unavailable. This could be because the Lodestone is under maintenance.")
