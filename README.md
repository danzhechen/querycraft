# querycraft 🔮

querycraft is an experiment in leveraging the RAG (Retrieval-Augmented Generation) framework for SQL generation. The goal is to automate SQL manipulation by enabling natural language inquiries to generate accurate SQL queries. This project uses the open-source LLM **llama-3.1-8b-instant** and has been tested on two databases of differing scales: **fruitmart** and **pagila**. The **fruitmart** database, created by Professor Mike Izbicki for in-class SQL quizzes, is a small dataset ideal for basic operations. The **pagila** database, a well-known PostgreSQL sample database, serves as a benchmark for more complex SQL use cases.

## Example Task

This is a relatively complicated task. The question prompt is:

**Compute the total revenue for each film.**

This simple question involves complicated hidden information, but the LLM successfully completed the task with the following query:

```sql
-- LLM Generated SQL
SELECT f.title, COALESCE(SUM(p.amount), 0.00) AS revenue FROM film f LEFT JOIN inventory i ON f.film_id = i.film_id LEFT JOIN rental r ON i.inventory_id = r.inventory_id LEFT JOIN payment p ON r.rental_id = p.rental_id GROUP BY f.title ORDER BY revenue DESC;
```

## Requirements

- Ensure that all dependencies listed in `requirements.txt` are installed before running the project.

- The project includes five test databases: `fruitmart`, `pagila`, `pagila-hw`, `pagila-hw2`, and `pagila-hw3`. Among those, `pagila-hw`, `pagila-hw2`, and `pagila-hw3` are specifically designed to evaluate SQL queries ranging from moderate to advanced complexity. To set up these test databases (excluding pagila), you will need to run `docker-compose up -d --build` in the respective directories. Each directory contains its own Docker configuration tailored for that database.

- Since pagila is configured as a submodule for `pagila-hw`, `pagila-hw2`, and `pagila-hw3`, you will also need to initialize and update the submodule by running the following commands:
```
git submodule init
git submodule update
```
## Interactive Mode

To run querycraft in interactive mode, use the following command:

```
python -m querycraft
```
- You can modify the database parameter to use fruitmart, or pagila-hw based on your requirements.
- In this mode, you can ask any natural language questions, and querycraft will generate the corresponding SQL query and return both the query and the results from the database.

## Tests

The tests in this project evaluate querycraft's ability to generate accurate SQL queries for a range of scenarios:

### [Fruitmart Tests](https://github.com/mikeizbicki/sql_quiz/tree/3bbc5adb55b1bc647534a27ff7de7a646b64b7dc)
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

#### [pagila-hw](https://github.com/mikeizbicki/pagila-hw/tree/7945f633e3fb30c5b522f5c383b1aa56aa7a514c)
- Covers basic SQL queries using the complex pagila schema.
- querycraft achieved a score of **16/17** on these tests, performing well for undergraduate-level tasks.

#### [pagila-hw2](https://gitlab.com/mikeizbicki/pagila-hw2)
- Includes more advanced SQL concepts such as:
  - `UNNEST` functions
  - Subqueries
  - Set operations
  - Arrays
- querycraft achieved a score of **8/18** on these tests, indicating room for improvement.

#### [pagila-hw3](https://github.com/mikeizbicki/pagila-hw3/)
- Focuses on highly complex SQL tasks, including:
  - More Nested subqueries
  - Advanced array manipulations
  - Detailed SQL knowledge
- querycraft achieved **1 pass** on this test, reflecting the challenging nature of these scenarios and areas for potential enhancement.

