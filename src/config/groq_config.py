import os
import time
import logging
from dotenv import load_dotenv
import groq
import re
from src.utils.schema_loader import SchemaLoader
from typing import Optional
from groq import InternalServerError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqConfig:
    SCHEMA_MAPPING = {
        "pagila-hw": "pagila",
        "pagila-hw2": "pagila",
        "pagila-hw3": "pagila"
    }
    
    def __init__(self, schema_name: str, max_retries: int = 3, retry_delay: float = 1.0):
        """Initialize GroqConfig with a specific schema
        
        Args:
            schema_name (str): Name of the schema to use
            
        Raises:
            ValueError: If no schema_name is provided or API key is missing
        """
        load_dotenv()
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = groq.Groq(api_key=self.api_key)
       
        available_schemas = SchemaLoader.list_available_schemas()

        if schema_name is None:
            raise ValueError(
                "Schema name must be provided. "
                f"Available schemas: {', '.join(available_schemas)}"
            )
        
        base_schema_name = self.SCHEMA_MAPPING.get(schema_name, schema_name)
        self.schema_name = schema_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.schema_loader = SchemaLoader(schema_name=base_schema_name)

    @staticmethod
    def _is_valid_sql(response: str) -> bool:
        """Check if response is pure SQL without markdown or explanations  
        
        >>> from src.config.groq_config import GroqConfig
        >>> GroqConfig._is_valid_sql("SELECT * FROM users;")
        True
        >>> GroqConfig._is_valid_sql("DELETE FROM users WHERE id = 1;")
        True
        >>> GroqConfig._is_valid_sql("WITH cte AS (SELECT * FROM users) SELECT * FROM cte;")
        True
        >>> GroqConfig._is_valid_sql("Here is the query: SELECT * FROM users;")
        False
        >>> GroqConfig._is_valid_sql("```sql\\nSELECT * FROM users;\\n```")
        False
        >>> GroqConfig._is_valid_sql("SELECT * FROM users; -- This is an explanation")
        True
        >>> GroqConfig._is_valid_sql("CREATE TABLE users (id INT, name TEXT);")
        False
        >>> GroqConfig._is_valid_sql("")
        False
        >>> GroqConfig._is_valid_sql("   ")
        False
        >>> GroqConfig._is_valid_sql("EXPLAIN SELECT * FROM users;")
        False
        """
        cleaned = response.strip().upper()
        sql_starters = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WITH']
        return any(cleaned.startswith(keyword) for keyword in sql_starters)
    
    def _clean_sql(self, sql: str) -> str:
        """Clean and standardize SQL query
    
        1. Extract only SQL if there's extra text
        2. Ensure semicolon at the end
        3. Standardize whitespace
        
        >>> obj = GroqConfig(schema_name="test_schema")
        >>> obj._clean_sql("SELECT * FROM table")
        'SELECT * FROM table;'
        
        >>> obj._clean_sql("  SELECT id, name FROM users   ")
        'SELECT id, name FROM users;'
        
        >>> obj._clean_sql("SELECT * FROM table;")
        'SELECT * FROM table;'
        
        >>> obj._clean_sql("SELECT * FROM table WHERE col ILIKE 'p%';")
        "SELECT * FROM table WHERE col ILIKE 'p%';"
        """
   
        sql = sql.replace('\\', '')

        sql = ' '.join(sql.split())
    
        if not sql.rstrip().endswith(';'):
            sql = f"{sql};"
    
        return sql

    def generate_sql(self, prompt: str) -> str:
        """
        Generate SQL query from natural language prompt
        
        Args:
        Returns:
            str: Generated SQL query
        """
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                schema_context = self.schema_loader.load_schema()
                examples = self.schema_loader.get_examples()

                system_prompt = f"""You are a SQL expert. Use this schema:

                {schema_context}

                Example queries:
                {examples}

                IMPORTANT:
                1. Return ONLY the raw SQL query - no markdown formatting, no explanations
                2. Do not wrap the query in ```sql``` blocks
                3. Do not include any text like "Here is the query:"
                4. Always use ILIKE instead of LIKE for case-insensitive text matching
                5. Always end queries with a semicolon
                6. Use simple ORDER BY without ASC (it's the default)
                7. Ensure exact schema column names are used
                8. Always specify the table name in the FROM clause
                9. Never use BETWEEN for date ranges - use >= and < instead
                10. Use subqueries only if absolutely necessary."""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]


                completion = self.client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",
                    temperature=0.05,
                    max_tokens=1000
                )

                response = completion.choices[0].message.content.strip()

                if not self._is_valid_sql(response):
                    if attempt < self.max_retries - 1:
                        continue
                    raise Exception("LLM response is not a valid SQL query")
                
                return self._clean_sql(response)

            except InternalServerError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                continue
            except Exception as e:
                raise Exception(f"Error generating SQL: {str(e)}")

        raise Exception(f"Error after {self.max_retries} retries: {str(last_exception)}")

    def test_connection(self) -> bool:
        """Test if Groq API connection is working"""
        try:
            self.generate_sql("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

    @classmethod
    def list_available_schemas(cls) -> list[str]:
        """List all available schemas"""
        return SchemaLoader.list_available_schemas()
