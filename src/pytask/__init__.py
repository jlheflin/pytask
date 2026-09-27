import argparse
from dataclasses import dataclass, field
from enum import Enum
import datetime
import rich

parser = argparse.ArgumentParser(
    prog="pytask",
    description="A python-based note/todo tracker",
    epilog="Text at the bottom of help"
)

parser.add_argument("args", nargs="*")

args = parser.parse_args().args

class Status(Enum):
    PENDING = "pending"
    DONE = "done"
    PAUSED = "paused"
    ACTIVE = "active"


class Priority(Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"

@dataclass
class Task:
    status: Status | None = None
    summary: str = ""
    notes: str = ""
    tags: set[str] = field(default_factory=set)
    project: str = ""
    priority: Priority = Priority.P2
    subtasks: list[Task] = field(default_factory=list)
    created: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now().astimezone()
    )
    due: datetime.datetime | None = None
    
        
def main() -> None:
    print("Hello from pytask!")
