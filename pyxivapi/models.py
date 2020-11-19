from dataclasses import dataclass

from .exceptions import XIVAPIInvalidFilter


@dataclass
class Filter:
    """
    Model class for DQL filters
    """
    field: str
    comparison: str
    value: int

    def __post_init__(self):
        if self.comparison.lower() not in ["gt", "gte", "lt", "lte"]:
            raise XIVAPIInvalidFilter(f'"{self.comparison}" is not a valid DQL filter comparison.')


@dataclass
class Sort:
    """
    Model class for sort field
    """
    field: str
    ascending: bool
