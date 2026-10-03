import argparse
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import datetime
import calendar
import os
import rich
import uuid
import json

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
        folders = [
            "pending",
            "done",
            "paused",
            "active"
        ]
        for folder in folders:
            path = PYTASK_CONFIG / folder
            path.mkdir(exist_ok=True)

parser = argparse.ArgumentParser(
    prog="pytask",
    description="A python-based note/todo tracker",
)
parser.add_argument("args", nargs="*")

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
    status: Status= Status.PENDING
    task_uuid: uuid.UUID = field(
        default_factory=lambda: uuid.uuid4
    )
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

    def write_task(self) -> None:
        path = (
            PYTASK_CONFIG.absolute() /
            self.status.value /
            f"{self.task_uuid}.json"
        )
        path.write_text(json.dumps(asdict(self), default=str, indent=4))

            

        

@dataclass
class TaskList:
    tasks: list[Task] = field(default_factory=list)

def create_date(text: str) -> datetime.datetime:
    text = text.strip().lower()
    today = datetime.datetime.today()

    if text == "today":
        return today
    if text == "tomorrow":
        return datetime.datetime.today() + datetime.timedelta(days=1)
    if text == "yesterday":
        return datetime.datetime.today() - datetime.timedelta(days=1)

    days = [d.lower() for d in calendar.day_name]
    if text in days:
        target = days.index(text)
        days_ahead = (target - today.weekday()) % 7 or 7
        return today + datetime.timedelta(days=days_ahead)

    if "-" in date:
        month, day = (int(x) for x in text.split("-"))
        candidate = today.replace(month=month, day=day)
        if candidate.date() < today.date():
            candidate = candidate.replace(year=today.year + 1)
        return candidate

    raise ValueError(f"Can't parse date: {text!r}")

def add_task(args: list[str]) -> None:
    tags = []
    summary = ""
    task = Task()

    for arg in args:
        if "project:" in arg:
            task.project: str = arg.split(":")[-1]
            args.remove(arg)
            continue
        if "due:" in arg:
            text = arg.split(":")[-1]
            task.due = create_date(text)
            args.remove(arg)
            continue
        if "+" in arg:
            tags.append(arg.replace("+", ""))
            args.remove(arg)
            continue


            
        
    task = Task(
        status=Status.PENDING,
    )

class TaskAction(Enum):
    ADD = task_add()

        
def main() -> None:
    args = parser.parse_args().args
    print(args)
