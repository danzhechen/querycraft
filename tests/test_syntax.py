import pytest
from src.config.groq_config import GroqConfig

def test_groq_connection():
    config = GroqConfig(schema_name="fruitmart")
    assert config.test_connection()

def test_sql_generation():
    config = GroqConfig(schema_name="fruitmart")
    prompt = "Show all products"
    sql = config.generate_sql(prompt)
    assert "SELECT" in sql.upper()
    assert "FROM" in sql.upper()

def test_sql_where_clause():
    config = GroqConfig(schema_name="fruitmart")
    prompt = "Find products with price greater than 100"
    sql = config.generate_sql(prompt)
    assert "WHERE" in sql.upper()
    assert ">" in sql or "GREATER" in sql.upper()

def test_sql_aggregation():
    config = GroqConfig(schema_name="fruitmart")
    prompt = "Calculate the total sales by category"
    sql = config.generate_sql(prompt)
    assert any(agg in sql.upper() for agg in ["SUM", "COUNT", "AVG"])
    assert "GROUP BY" in sql.upper()

def test_sql_order_by():
    config = GroqConfig(schema_name="fruitmart")
    prompt = "List customers ordered by their total purchases"
    sql = config.generate_sql(prompt)
    assert "ORDER BY" in sql.upper()
