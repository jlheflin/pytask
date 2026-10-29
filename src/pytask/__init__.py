from rich.console import Console
from rich.text import Text
import sqlite3
import argparse
from pathlib import Path
import os
from .schema import schema
from uuid import uuid4
from datetime import date
from pprint import pp

DB_PATH = Path(
    os.getenv("PYTASK_DB_PATH") or
    Path().home() / ".pytask" / "pytask.db"
)

def get_connection() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    return con

if not DB_PATH.exists():
    print("Initializing pytask database...")
    print(f"pytask database location: {DB_PATH}")
    prompt: str = f"Would you like to create a database in this location? [Y/n]: "
    ans: str = input(prompt).strip().lower()
    if ans not in ("", "y", "yes"):
        raise SystemExit("Aborted: no database created")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as con:
        con.executescript(schema)

attribute_list = [
    "due",
    "project"
]


def print_tasks(task_inputs):
    with get_connection() as db:
        rows = db.execute("SELECT * FROM Taskset WHERE is_deleted = 0 AND is_completed = 0").fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No tasks yet! Add them via pytask add")

def add_task(task_inputs):
    tags: list[str] = [i for i in task_inputs if i.startswith('+')]
    words = [w for w in task_inputs if not w.startswith('+') and ":" not in w]
    attributes = [a for a in task_inputs if ':' in a and a.split(':')[0] in attribute_list]
    with get_connection() as db:
        rows = db.execute("SELECT display_id FROM Taskset WHERE display_id IS NOT NULL").fetchall()
        display_ids: list[int] = [display_id[0] for display_id in rows]
        summary = " ".join(words)
        if not display_ids:
            display_id = 1
        else:
            max_id = max(display_ids)
            avail_ids = [i for i in range(1, max_id) if i not in display_ids]
            if not avail_ids:
                display_id = max_id + 1
            else:
                display_id = min(avail_ids)
        db.execute(
            """
                INSERT INTO Taskset (
                    display_id,
                    task_uuid,
                    summary,
                    created_date
                ) VALUES (?,?,?,?)
            """,
            (display_id, str(uuid4()), summary, date.today())
        )
        for tag in tags:
            name = tag[1:]
            row = db.execute(
                "SELECT tag_id FROM Tag WHERE tag_name = ?",
                (name,)
            ).fetchone()
            if row:
                tag_id = row[0]
            else:
                tag_id = (
                    row[0] if row else db.execute("INSERT INTO Tag (tag_name) VALUES (?)", (name,))
                ).lastrowid
            
    print(f"Added task {display_id} {summary}")

def remove_task(task_list):
    task_list = [int(t) for t in task_list]
    with get_connection() as db:
        rows = db.execute("SELECT display_id FROM Taskset").fetchall()
        display_ids = [display_id[0] for display_id in rows]
        for task in task_list:
            if task not in display_ids:
                raise ValueError(f"{task} not in task IDs")
        for task in task_list:
            db.execute(
                "UPDATE Taskset SET is_deleted = 1, display_id = NULL, resolved_date = ? WHERE display_id = ?",
                (date.today().isoformat(), task)
            )

    print("Removing task")

def modify_task(task_inputs):
    print(task_inputs)
    print("Modifying task")

def note_task(task_list):
    print(task_list)
    print("Adding note to task")

def edit_task(task_list):
    print(task_list)
    print("Editing task")

action_set = {
    "next": print_tasks,
    "add": add_task,
    "remove": remove_task,
    "modify": modify_task,
    "note": note_task,
    "edit": edit_task
}

parser = argparse.ArgumentParser(
    prog='pytask',
    description='A task manager and note taking app',
)
parser.add_argument("action", choices=action_set, nargs="?", default="next")
parser.add_argument("inputs", nargs="*")

def main():
    console = Console()
    args = parser.parse_args()
    if args.action == None:
        args.action = "next"
    action_set[args.action](args.inputs)

if __name__ == '__main__':
    main()
