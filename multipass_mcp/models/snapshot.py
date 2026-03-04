from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass
class MultipassSnapshot:
    instance: str
    name: str
    comment: str = ''
    parent: str = ''


@dataclass
class MultipassSnapshotInfo:
    instance: str
    name: str
    comment: str = ''
    cpu_count: str = ''
    created: str = ''
    disk_space: str = ''
    memory_size: str = ''
    mounts: dict[str, Any] = field(default_factory=dict)
    parent: str = ''
    size: str = ''
