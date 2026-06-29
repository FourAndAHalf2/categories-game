from typing import Callable, Optional
from cached_get import cached_get


class Category:
    def __init__(
        self,
        name: str,
        url: Optional[str] = None,
        fetch_function: Optional[Callable] = None,
        parser: Optional[Callable] = None,
        cache_duration: int = -1,
    ) -> None:
        self.name = name
        self.url = url
        self._fetch_function = fetch_function
        self.parser = parser or (lambda raw: raw)
        self.cache_duration = cache_duration

    def fetch_raw(self):
        if self._fetch_function is not None:
            return self._fetch_function()
        if self.url is None:
            raise ValueError("No url or fetch_function provided for category")
        return cached_get(self.url, cache_duration=self.cache_duration)

    def get_items(self):
        raw = self.fetch_raw()
        return self.parser(raw)
