import pytest
from querycraft.config.groq_config import GroqConfig

def test_sql_generation():
    config = GroqConfig(schema_name="fruitmart")
    prompt = "Show all products"
    sql = config.generate_sql(prompt)
    assert "SELECT" in sql.upper()
    assert "FROM" in sql.upper()

def test_sql_order_by():
    config = GroqConfig(schema_name="fruitmart")
    prompt = "List customers ordered by their total purchases"
    sql = config.generate_sql(prompt)
    assert "ORDER BY" in sql.upper()
