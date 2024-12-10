# querycraft 🔮

querycraft is an experiment in leveraging the RAG (Retrieval-Augmented Generation) framework for SQL generation. The goal is to automate SQL manipulation by enabling natural language inquiries to generate accurate SQL queries. This project uses the open-source LLM **llama-3.1-8b-instant** and has been tested on two databases of differing scales: **fruitmart** and **pagila**. The **fruitmart** database, created by Professor Mike Izbicki for in-class SQL quizzes, is a small dataset ideal for basic operations. The **pagila** database, a well-known PostgreSQL sample database, serves as a benchmark for more complex SQL use cases.

## Requirements

- Ensure that all dependencies listed in `requirements.txt` are installed before running the project.

- The project includes five test databases: `fruitmart`, `pagila`, `pagila-hw`, `pagila-hw2`, and `pagila-hw3`. Among those, `pagila-hw`, `pagila-hw2`, and `pagila-hw3` are specifically designed to evaluate SQL queries ranging from moderate to advanced complexity. To set up these test databases (excluding pagila), you will need to run `docker-compose up -d --build` in the respective directories. Each directory contains its own Docker configuration tailored for that database.

- Since pagila is configured as a submodule for `pagila-hw`, `pagila-hw2`, and `pagila-hw3`, you will also need to initialize and update the submodule by running the following commands:
```
git submodule init
git submodule update
```

## Tests

The tests in this project evaluate querycraft's ability to generate accurate SQL queries for a range of scenarios:

### Fruitmart Tests
- Examine basic SQL operations such as `COUNT`, handling `NULL` values, and `GROUP BY`.
- Test slightly more advanced queries involving case-insensitive matching using `ILIKE`.
- These tests are located in the `tests` directory and can be executed using the following commands:
```
pytest tests/test_syntax.py
pytest tests/test_sql_generation_fruitmart.py
pytest tests/test_natural_queries_fruitmart.py
```
querycraft successfully passes all these tests.

### Pagila Tests
- The pagila tests are set up differently from fruitmart and focus on more complex SQL scenarios. The tests are based on three additional directories in the `test_databases folder`: `pagila-hw`, `pagila-hw2`, and `pagila-hw3`. These directories are derived from SQL homework assignments for a Big Data class, designed for undergraduate-level complexity.
- A `run_tests.sh script` is provided in each directory to streamline the testing process. After setting up Docker for PostgreSQL, you can run the script to execute the tests automatically.

#### pagila-hw
- Covers basic SQL queries using the complex pagila schema.
- querycraft achieved a score of **16/17** on these tests, performing well for undergraduate-level tasks.

#### pagila-hw2
- Includes more advanced SQL concepts such as:
  - `UNNEST` functions
  - Subqueries
  - Set operations
  - Arrays
- querycraft achieved a score of **8/18** on these tests, indicating room for improvement.

#### pagila-hw3
- Focuses on highly complex SQL tasks, including:
  - More Nested subqueries
  - Advanced array manipulations
  - Detailed SQL knowledge
- querycraft achieved **1 pass** on this test, reflecting the challenging nature of these scenarios and areas for potential enhancement.

