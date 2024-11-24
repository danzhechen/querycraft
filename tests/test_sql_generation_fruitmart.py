import pytest
import re
from src.config.groq_config import GroqConfig
from groq import InternalServerError
from src.utils.schema_loader import SchemaLoader

@pytest.fixture
def groq_config():
    return GroqConfig(
        schema_name="fruitmart"
    )

@pytest.mark.skip_on_api_error
def test_basic_counting(groq_config):
    test_cases = [
        {
            "prompt": "Count all rows in basket B",
            "expected_sql": "SELECT count(*) FROM basket_b;"
        },
        {
            "prompt": "How many unique fruits are in basket B?",
            "expected_sql": "SELECT count(DISTINCT fruit_b) FROM basket_b;"
        }
    ]
    
    for case in test_cases:
        try:
            generated_sql = groq_config.generate_sql(case["prompt"])
            generated_sql = " ".join(generated_sql.upper().split())
            expected_sql = " ".join(case["expected_sql"].upper().split())
            assert generated_sql == expected_sql
        except InternalServerError as e:
            pytest.skip(f"Groq API unavailable: {str(e)}")

def test_null_handling(groq_config):
    test_cases = [
        {
            "prompt": "Count rows where fruit is null in basket B",
            "expected_sql": "SELECT count(*) FROM basket_b WHERE fruit_b IS NULL;"
        },
        {
            "prompt": "Count rows where fruit is not null in basket B",
            "expected_sql": "SELECT count(*) FROM basket_b WHERE fruit_b IS NOT NULL;"
        },
        {
            "prompt": "Count only the rows where ID is not null in basket B",
            "expected_sql": "SELECT COUNT(*) FROM basket_b WHERE id IS NOT NULL;"
        }
    ]
    
    for case in test_cases:
        try:
            generated_sql = groq_config.generate_sql(case["prompt"])
            generated_sql = " ".join(generated_sql.upper().split())
            expected_sql = " ".join(case["expected_sql"].upper().split())
            assert generated_sql == expected_sql
        except InternalServerError as e:
            pytest.skip(f"Groq API unavailable: {str(e)}")

def test_group_by(groq_config):
    test_cases = [
        {
            "prompt": "Show count of each fruit in basket B, ordered by fruit name",
            "expected_sql": """
                SELECT fruit_b, count(*)
                FROM basket_b
                GROUP BY fruit_b
                ORDER BY fruit_b;
            """
        },
        {
            "prompt": "Show fruits that appear more than once in basket B",
            "expected_sql": """
                SELECT fruit_b, count(*)
                FROM basket_b
                GROUP BY fruit_b
                HAVING count(*) > 1
                ORDER BY fruit_b;
            """
        }
    ]
    
    for case in test_cases:
        try:
            generated_sql = groq_config.generate_sql(case["prompt"])
            generated_sql = " ".join(generated_sql.upper().split())
            expected_sql = " ".join(case["expected_sql"].upper().split())
            assert generated_sql == expected_sql
        except InternalServerError as e:
            pytest.skip(f"Groq API unavailable: {str(e)}")

def test_complex_questions(groq_config):
    test_cases = [
        {
            "prompt": "Which fruits in basket A contain the letter 'a' (case insensitive)?",
            "expected_sql": "SELECT fruit_a FROM basket_a WHERE fruit_a ILIKE '%a%';"
        },
        {
            "prompt": "Find all fruits in basket A that start with 'p' (ignore case)",
            "expected_sql": "SELECT fruit_a FROM basket_a WHERE fruit_a ILIKE 'p%';"
        },
        {
            "prompt": "Show fruits from basket A that end with 'y' (case insensitive)",
            "expected_sql": "SELECT fruit_a FROM basket_a WHERE fruit_a ILIKE '%y';"
        }
    ]

    for case in test_cases:
        try:
            generated_sql = groq_config.generate_sql(case["prompt"])
            assert generated_sql.strip() == case["expected_sql"].strip(), (
                f"SQL doesn't match for prompt: {case['prompt']}\n"
                f"Expected: {case['expected_sql']}\n"
                f"Got: {generated_sql}"
            )
        except Exception as e:
            pytest.fail(f"Error for prompt '{case['prompt']}': {str(e)}")
