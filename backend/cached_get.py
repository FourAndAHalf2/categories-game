from requests import get
from datetime import datetime, timedelta
from hashlib import sha256
from os.path import isfile
from pathlib import Path
from json import load, dump
from time import time
from glob import glob

cache = {}


def cached_get(url: str, cache_duration=10, headers: dict | None = None) -> str:
    if headers is None:
        headers = {}

    now = datetime.now()

    entry = cache.get(url)
    if entry and entry["expiry"] > now:
        return entry["content"]

    hash_of_url = sha256(url.encode()).hexdigest()

    cache_directory = Path(__file__).parent / "data" / "cache"
    cache_directory.mkdir(parents=True, exist_ok=True)

    for file_path in cache_directory.glob(f"{hash_of_url}.*"):
        try:
            timestamp = int(file_path.suffix[1:])
        except ValueError:
            continue

        if timestamp > time():
            content = file_path.read_text(encoding="utf-8")

            cache[url] = {
                "content": content,
                "expiry": datetime.fromtimestamp(timestamp),
            }

            return content
        else:
            file_path.unlink(missing_ok=True)

    # Pobieranie z internetu
    response = get(url, headers=headers)
    response.raise_for_status()

    expiry_timestamp = int(time() + 60 * cache_duration)
    cache_file_path = cache_directory / f"{hash_of_url}.{expiry_timestamp}"

    cache_file_path.write_text(response.text, encoding="utf-8")

    cache[url] = {
        "content": response.text,
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
        response = get(url, headers=headers)

        data = response.text
        with open(path, "w") as file:
            dump(data, file)

    return data
