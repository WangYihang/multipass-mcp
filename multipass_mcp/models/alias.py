from dataclasses import dataclass


@dataclass
class MultipassAlias:
    name: str
    instance: str
    command: str
    working_directory: str
    context: str
