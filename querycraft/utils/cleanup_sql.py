# querycraft/utils/cleanup_sql.py

from pathlib import Path
import sys

def cleanup_sql_file(file_path: Path) -> None:
    """Remove LLM marker and generated SQL from a file"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Keep lines until LLM marker (excluding the marker)
    cleaned_lines = []
    for line in lines:
        if line.strip() == "-- LLM Generated SQL":
            break
        cleaned_lines.append(line)
    
    # Write back cleaned content
    with open(file_path, 'w') as file:
        file.writelines(cleaned_lines)

def cleanup_schema_files(schema_name: str) -> None:
    """Clean all SQL files in schema directory"""
    sql_folder = Path("test_databases") / schema_name / "sql"
    if not sql_folder.exists():
        print(f"Schema folder not found: {sql_folder}")
        return
    
    for sql_file in sql_folder.glob("*.sql"):
        print(f"Cleaning {sql_file.name}...")
        cleanup_sql_file(sql_file)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cleanup_sql.py <schema_name>")
        sys.exit(1)
        
    schema_name = sys.argv[1]
    cleanup_schema_files(schema_name)