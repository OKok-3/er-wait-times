from abc import ABC, abstractmethod


class BaseScraper(ABC):
    _id: str
    name: str
    dept: str
    address: str
    county: str
    city: str
    province: str
    url: str
    version: int

    def __init__(self, metadata: dict[str, any]):
        self._id = metadata["id"]
        self.name = metadata["name"]
        self.dept = metadata["dept"]
        self.address = metadata["address"]
        self.county = metadata["county"]
        self.city = metadata["city"]
        self.province = metadata["province"]
        self.url = metadata["url"]
        self.version = metadata["version"]

    @abstractmethod
    def scrape(self, ts: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def parse(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self) -> None:
        raise NotImplementedError
