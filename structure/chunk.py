from dataclasses import dataclass
from structure.source import Source
@dataclass(frozen=True)
class Chunk:
    page : int
    index : int
    text: str
    source : Source