from abc import ABC, abstractmethod


class BaseScraper(ABC):
    _id: str
    name: str
    dept: str
    address: str
    county: str
    city: str
    province: str
    timezone: str
    url: str
    scraper_module: str
    scraper_class: str
    version: int

    def __init__(self, metadata: dict[str, any]):
        self._id = metadata["id"]
        self.name = metadata["name"]
        self.dept = metadata["dept"]
        self.address = metadata["address"]
        self.county = metadata["county"]
        self.city = metadata["city"]
        self.province = metadata["province"]
        self.timezone = metadata["timezone"]
        self.url = metadata["url"]
        self.scraper_module = metadata["scraper_module"]
        self.scraper_class = metadata["scraper_class"]
        self.version = metadata["version"]

    @abstractmethod
    def scrape(self, ts: str) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def parse(self, data: dict[str, str]) -> dict[str, any]:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: dict[str, any]) -> None:
        raise NotImplementedError
