import os
import time
from dotenv import load_dotenv
import groq
import re
from src.utils.schema_loader import SchemaLoader
from typing import Optional
from groq import InternalServerError

class GroqConfig:
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
        
        self.schema_loader = SchemaLoader(schema_name=schema_name)
        self.max_retries = max_retries
        self.retry_delay = retry_delay

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
                1. Return ONLY the SQL query, no explanations or additional text
                2. Always use ILIKE instead of LIKE for case-insensitive text matching
                2. Always end queries with a semicolon
                3. Use simple ORDER BY without ASC (it's the default)
                4. Ensure exact schema column names are used
                5. Always specify the table name in the FROM clause"""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]


                completion = self.client.chat.completions.create(
                    messages=messages,
                    model="mixtral-8x7b-32768",
                    temperature=0.1,
                    max_tokens=1000
                )

                return self._clean_sql(completion.choices[0].message.content.strip())

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
