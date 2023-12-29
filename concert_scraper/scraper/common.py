from dataclasses import dataclass


@dataclass
class Concert:
    title: str
    date: str
    venue: str
    url: str

    def __hash__(self) -> int:
        return hash(self.url)


@dataclass
class Venue:
    name: str
    location: str
    type: str
    url: str
