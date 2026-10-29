

schema = """
CREATE TABLE Taskset (
    id INTEGER PRIMARY KEY,
    display_id INTEGER,
    task_uuid TEXT NOT NULL UNIQUE,
    summary TEXT DEFAULT '',
    note TEXT DEFAULT '',
    created_date TEXT NOT NULL,
    resolved_date TEXT,
    is_completed INTEGER NOT NULL DEFAULT 0 CHECK(is_completed IN (0, 1)),
    is_deleted INTEGER NOT NULL DEFAULT 0 CHECK(is_deleted IN (0, 1))
);
CREATE UNIQUE INDEX open_display_id ON Taskset(display_id) WHERE display_id IS NOT NULL;
CREATE TABLE Tag (
    tag_id INTEGER PRIMARY KEY,
    tag_name TEXT NOT NULL UNIQUE
);
CREATE TABLE TasksetTag (
    taskset_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (taskset_id, tag_id),
    FOREIGN KEY (taskset_id) REFERENCES Taskset(id),
    FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
);
CREATE TABLE Project (
    project_id INTEGER NOT NULL,
    project_name TEXT NOT NULL UNIQUE
);
CREATE TABLE TasksetProject (
    taskset_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    PRIMARY KEY (taskset_id, project_id),
    FOREIGN KEY (taskset_id) REFERENCES Taskset(id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
);
"""
