from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass
class MultipassInstance:
    name: str
    state: str
    ipv4: list[str]
    release: str


@dataclass
class MultipassInfo:
    name: str
    state: str
    ipv4: list[str]
    release: str
    image_hash: str = ''
    load: list[float] = field(default_factory=list)
    disk_usage: dict[str, str] = field(default_factory=dict)
    memory_usage: dict[str, str] = field(default_factory=dict)
    mounts: dict[str, Any] = field(default_factory=dict)
