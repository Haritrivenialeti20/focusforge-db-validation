from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parents[1]
schema = (root / 'schema/schema.sql').read_text()
schema_sqlite = schema.replace('VARCHAR(100)', 'TEXT').replace('VARCHAR(255)', 'TEXT')
valid = (root / 'schema/sample_data.sql').read_text()
invalid_cases = [
    ('NOT NULL', "INSERT INTO tasks (id, title, priority, project_id) VALUES (3, NULL, 3, 1);"),
    ('UNIQUE', "INSERT INTO users (id, name, email) VALUES (3, 'Charlie', 'alice@email.com');"),
    ('CHECK', "INSERT INTO tasks (id, title, priority, project_id) VALUES (4, 'Testing Task', 10, 1);"),
    ('FOREIGN KEY', "INSERT INTO tasks (id, title, priority, project_id) VALUES (5, 'Ghost Task', 2, 999);"),
]

def fresh():
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.executescript(schema_sqlite)
    conn.executescript(valid)
    return conn

valid_conn = fresh()
assert valid_conn.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 2
assert valid_conn.execute('SELECT COUNT(*) FROM projects').fetchone()[0] == 2
assert valid_conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0] == 2
print('valid sample data: accepted (2 users, 2 projects, 2 tasks)')

for label, sql in invalid_cases:
    conn = fresh()
    try:
        conn.execute(sql)
    except sqlite3.IntegrityError as exc:
        print(f'{label}: rejected — {exc}')
    else:
        raise AssertionError(f'{label} case was accepted')

(root / 'docs/verification-output.txt').write_text('valid sample data: accepted\n' + '\n'.join(f'{label}: rejected' for label, _ in invalid_cases) + '\n')
print('verification passed: all four invalid writes were rejected')
