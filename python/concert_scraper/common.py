from dataclasses import dataclass


@dataclass
class Concert:
    title: str
    date: str
    venue: str
    url: str

    def __hash__(self) -> int:
        return hash(self.url)

    def __str__(self):
        return f"{self.venue}: {self.title} - {self.date}"


@dataclass
class Venue:
    name: str
    location: str
    type: str
    url: str
