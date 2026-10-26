-- FocusForge constrained PostgreSQL schema

DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE projects (
    id INT PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL
);

CREATE TABLE tasks (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    priority INT NOT NULL CHECK (priority BETWEEN 1 AND 5),
    project_id INT NOT NULL,
    CONSTRAINT tasks_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES projects(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX idx_tasks_project_id ON tasks(project_id);
