# FocusForge Database-Level Validation

This submission hardens the supplied FocusForge schema against direct SQL writes. It keeps the valid sample data unchanged while making invalid records impossible to store.

## Constraint coverage

- `NOT NULL`: user names and emails, project names, and task titles; task priority and project reference are also required.
- `UNIQUE`: `users.email` prevents duplicate login identities.
- `CHECK`: task priority must be between 1 and 5.
- `FOREIGN KEY`: every task `project_id` must reference an existing project.

## Files

- `schema/schema.sql` — corrected PostgreSQL schema.
- `schema/sample_data.sql` — supplied valid records, unchanged.
- `schema/invalid_data.sql` — supplied four invalid inserts, unchanged.
- `schema/constraints_test.sql` — named test copy for the challenge workflow.
- `schema/schema.original.sql` — supplied unconstrained schema for comparison.
- `Observations.md` — findings, rationale, and results.
- `docs/screenshots/` — one rejection artifact per constraint test.
- `scripts/verify_constraints.py` — reproducible valid-data and rejection test harness.

## PostgreSQL workflow

```bash
createdb focusforge
psql -d focusforge -f schema/schema.sql
psql -d focusforge -f schema/sample_data.sql
psql -d focusforge -f schema/constraints_test.sql
```

The sample data completes successfully. Each test statement is expected to stop with a PostgreSQL constraint violation. To isolate the four failures, reset the database or run each statement in a transaction that is rolled back after observing the error.

## Verification

```bash
python3 scripts/verify_constraints.py
```

The harness runs the valid sample inserts, then rebuilds a fresh constrained database for each invalid statement and confirms the expected `NOT NULL`, `UNIQUE`, `CHECK`, and foreign-key failures.
