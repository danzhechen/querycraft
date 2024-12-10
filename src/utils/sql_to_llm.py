import os
import sys
from pathlib import Path
from src.config.groq_config import GroqConfig

def read_sql_files(sql_folder):
    sql_files = Path(sql_folder).glob("*.sql")
    sql_contents = {}
    for sql_file in sql_files:
        with open(sql_file, 'r') as file:
            sql_contents[sql_file.name] = file.read()
    return sql_contents

def append_llm_output(sql_folder, file_name, content):
    output_path = Path(sql_folder) / file_name
    with open(output_path, 'a') as file:
        file.write("\n-- LLM Generated SQL\n")
        file.write(content)

def main(schema_name):
    sql_folder = Path("test_databases") / schema_name / "sql"

    groq_config = GroqConfig(schema_name=schema_name)
    sql_contents = read_sql_files(sql_folder)

    for file_name, sql_content in sql_contents.items():
        print(f"Processing {file_name}...")
        llm_output = groq_config.generate_sql(sql_content)
        append_llm_output(sql_folder, file_name, llm_output)
        print(f"Output appended to {sql_folder / file_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sql_to_llm.py <schema_name>")
        sys.exit(1)
    
    schema_name = sys.argv[1]
    main(schema_name)