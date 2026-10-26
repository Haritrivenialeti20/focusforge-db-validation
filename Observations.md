# FocusForge DB-Level Validation Observations

## Issues found

The original schema had primary keys but no database-level rules for required values, identity, numeric ranges, or relationships. As a result, the invalid-data script could insert a task with a NULL title, a second user with Alice's email, a priority of 10, and a task pointing at project 999. These defects could enter through direct SQL, migrations, seed scripts, or third-party integrations without passing API validation.

## Constraints implemented

- `NOT NULL` on `users.name`, `users.email`, `projects.project_name`, `tasks.title`, `tasks.priority`, and `tasks.project_id` prevents incomplete records and relationship gaps.
- `UNIQUE` on `users.email` guarantees that email is a stable identity for login and account lookup.
- `CHECK (priority BETWEEN 1 AND 5)` enforces the FocusForge priority domain at the database boundary.
- `FOREIGN KEY (tasks.project_id) REFERENCES projects(id)` rejects orphan tasks. `ON DELETE RESTRICT` prevents deleting a project while tasks still depend on it.
- An index on `tasks.project_id` keeps project task lookups efficient without weakening integrity.

## Verification result

The unchanged valid sample data inserts successfully. Each invalid case was executed against a fresh constrained database so one failure could not affect the next case:

1. NULL task title — rejected by `NOT NULL`.
2. Duplicate Alice email — rejected by `UNIQUE`.
3. Priority 10 — rejected by `CHECK`.
4. Project 999 — rejected by the foreign key.

The four screenshot artifacts capture the rejection class and the offending statement. The Python harness reproduces all checks with foreign-key enforcement enabled; the SQL remains PostgreSQL-compatible and can be run with `psql` as shown in the README.
