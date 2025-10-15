from abc import ABC, abstractmethod


class BaseScraper(ABC):
    name: str
    location: str
    address: str
    _id: str
    url: str
    dept: str
    version: int

    def __init__(self, name: str, _id: str, location: str, address: str, id: str, url: str, dept: str, version: int):
        self.name = name
        self._id = _id
        self.location = location
        self.address = address
        self.url = url
        self.dept = dept
        self.version = version

    @abstractmethod
    def scrape(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def parse(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self) -> None:
        raise NotImplementedError
