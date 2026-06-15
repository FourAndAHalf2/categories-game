from requests import get
from requests import Response
from datetime import datetime, timedelta
from hashlib import sha256
from os.path import isfile
from pathlib import Path
from json import load, dump

cache = {}


def cached_get(url: str, cache_duration=10, headers: dict | None = None) -> str:
    """# Fetching and caching dynamic data of a website

    Args:
        url (str): url of website to fetch
        cache_duration (int, optional): time (in minutes) in cached data is used in caching. Defaults to 10.
        headers (dict | None, optional): headers used while fetching data. Defaults to None.

    Returns:
        str: _description_
    """

    if headers is None:
        headers = {}

    now = datetime.now()
    entry = cache.get(url)

    # return valid cached response
    if entry is not None and entry.get("expiry") is not None and entry["expiry"] > now:
        return entry["response"]

    response = get(url, headers=headers)

    if response.status_code == 200:
        cache[url] = {
            "response": response.text,
            "expiry": now + timedelta(minutes=cache_duration),
        }

    return response.text

def cached_get_static(url: str, headers: dict | None = None) -> str:
    """# Fetching and caching static data of a website

    after fetching given url, the results are saved in `data/cache` directory if http code is 200

    Args:
        url (str): url of website to fetch
        headers (dict | None, optional): headers used while fetching data. Defaults to None.

    Returns:
        str: result of the fetch
    """

    data = []
    path = Path(__file__).parent / "data" / "cache" / sha256(url.encode()).hexdigest()
    if isfile(path):
        with open(path) as file:
            data = load(file)
    else:
        response = get(
            url
        )

        data = response.text
        with open(path, "w") as file:
            dump(data, file)

    return data
