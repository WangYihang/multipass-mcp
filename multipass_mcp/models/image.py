from dataclasses import dataclass


@dataclass
class MultipassImage:
    name: str
    aliases: list[str]
    os: str
    release: str
    remote: str
    version: str
