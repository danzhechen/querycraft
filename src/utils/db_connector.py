import subprocess
from pathlib import Path
import os
import logging
from src.config.groq_config import GroqConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnector:
    def __init__(self, schema_name: str = "fruitmart"):
        """Initialize database connector
        
        Args:
            schema_name (str): Name of the schema/database directory
        """
        self.project_root = Path(os.getcwd())
        self.db_path = self.project_root / "test_databases" / schema_name
        self.groq_config = GroqConfig(schema_name=schema_name)
        logger.info(f"Database path: {self.db_path}")

    def execute_sql(self, sql_query: str) -> str:
        """Execute a SQL query using docker-compose and psql
        
        Args:
            sql_query (str): SQL query to execute
            
        Returns:
            str: Query results
        """
        try:
            original_dir = os.getcwd()
            os.chdir(self.db_path)

            logger.info(f"Executing in directory: {os.getcwd()}")
    
            command = f'docker-compose exec -T pg psql -U postgres -t -A -c "{sql_query}"'

            logger.info(f"Executing command: {command}")

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            os.chdir(original_dir)
            
            logger.info(f"Raw stdout: '{result.stdout}'")
            logger.info(f"Raw stderr: '{result.stderr}'")

            if result.returncode != 0:
                logger.error(f"SQL Error: {result.stderr}")
                raise Exception(f"SQL execution failed: {result.stderr}")
                
            rows = result.stdout.strip().split('\n')
            if len(rows) == 1 and not rows[0]:
                return "No results found"
            return "\n".join(rows)

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise
        
        finally:
            if 'original_dir' in locals():
                os.chdir(original_dir)

    
    def execute_natural_query(self, question: str) -> dict:
        """Execute a natural language query
        
        Args:
            question (str): Natural language question
            
        Returns:
            dict: Contains question, SQL, and results
        """
        try:
            sql_query = self.groq_config.generate_sql(question)
            logger.info(f"Generated SQL: {sql_query}")
            
            result = self.execute_sql(sql_query) 
    
            return {
                "question": question,
                "sql_query": sql_query,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error executing natural query: {e}")
            raise

    def interactive_mode(self):
        """Start interactive query mode"""
        print("Welcome to SQL Query Assistant!")
        print("Type 'exit' to quit")
        
        while True:
            question = input("\nEnter your question: ").strip()
            
            if question.lower() == 'exit':
                break
                
            try:
                result = self.execute_natural_query(question)
                print("\nGenerated SQL:", result["sql_query"])
                print("Result:", result["result"])
            except Exception as e:
                print(f"Error: {e}")


    def test_connection(self) -> bool:
        """Test if database connection is working"""
        try:
            result = self.execute_sql("SELECT 1;")
            return result.strip() == "1"
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
