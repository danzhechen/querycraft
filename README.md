# querycraft 🔮

querycraft is an experiment in leveraging the RAG (Retrieval-Augmented Generation) framework for SQL generation. The goal is to automate SQL manipulation by enabling natural language inquiries to generate accurate SQL queries. This project uses the open-source LLM **llama-3.1-8b-instant** and has been tested on two databases of differing scales: **fruitmart** and **pagila**. The **fruitmart** database, created by Professor Mike Izbicki for in-class SQL quizzes, is a small dataset ideal for basic operations. The **pagila** database, a well-known PostgreSQL sample database, serves as a benchmark for more complex SQL use cases.

## Requirements

1. Ensure that all dependencies listed in `requirements.txt` are installed before running the project.

2. The project includes five test databases: `fruitmart`, `pagila`, `pagila-hw`, `pagila-hw2`, and `pagila-hw3`. Among those, `pagila-hw`, `pagila-hw2`, and `pagila-hw3` are specifically designed to evaluate SQL queries ranging from moderate to advanced complexity. To set up these test databases (excluding pagila), you will need to run `docker-compose up -d --build` in the respective directories. Each directory contains its own Docker configuration tailored for that database.

3. Since pagila is configured as a submodule for `pagila-hw`, `pagila-hw2`, and `pagila-hw3`, you will also need to initialize and update the submodule by running the following commands:
```
git submodule init
git submodule update
```

## Tests

The tests in this project evaluate querycraft's ability to generate accurate SQL queries for a range of scenarios:

- **Fruitmart Tests**:
  - Examine basic SQL operations such as `COUNT`, handling `NULL` values, and `GROUP BY`.
  - Test slightly more advanced queries involving case-insensitive matching using `ILIKE`.

Further tests for **pagila** database operations and advanced SQL functionalities will be included in future iterations.
