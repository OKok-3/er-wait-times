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

    def __init__(
        self,
        _id: str,
        name: str,
        dept: str,
        address: str,
        county: str,
        city: str,
        province: str,
        url: str,
        version: int,
    ):
        self._id = _id
        self.name = name
        self.dept = dept
        self.address = address
        self.county = county
        self.city = city
        self.province = province

    @abstractmethod
    def scrape(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def parse(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self) -> None:
        raise NotImplementedError
