import argparse
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import datetime
import os
import rich


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

@dataclass
class TaskList:
    tasks: list[Task] = field(default_factory=list)

    

env_path = os.getenv("PYTASK_CONFIG")
if env_path:
    PYTASK_CONFIG = Path(env_path).expanduser()
else:
    PYTASK_CONFIG = Path.home() / ".pytask"

if not PYTASK_CONFIG.exists():
    ans = input(f"Running first time setup, okay to create {PYTASK_CONFIG.absolute()}? [y/N]: ")
    if ans == "" or ans.lower() == "n":
        err = f"""\
        Not creating {PYTASK_CONFIG.absolute()} due to user denial.
        """
        raise RuntimeError(err)
    elif ans != "" and ans.lower() != "y":
        raise ValueError(f"Invalid input.")
    elif ans.lower() == "y": 
        PYTASK_CONFIG.mkdir(exist_ok=True)

parser = argparse.ArgumentParser(
    prog="pytask",
    description="A python-based note/todo tracker",
)
parser.add_argument("args", nargs="*")
        
def main() -> None:
    args = parser.parse_args().args
    print(args)
