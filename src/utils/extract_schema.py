def extract_schema(file_path):
    """
    Extract CREATE TABLE and CREATE VIEW statements from Pagila schema file
    Returns a list of SQL statements
    """
    sql_statements = []
    current_statement = []
    is_collecting = False
   
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith('--') or not line.strip():
                continue
                
            if line.strip().startswith('CREATE TABLE') or line.strip().startswith('CREATE VIEW'):
                is_collecting = True
                current_statement = [line]
                continue
                
            if is_collecting:
                current_statement.append(line)
                if ');' in line:
                    clean_statement = ''.join(current_statement)
                    if 'ALTER' not in clean_statement:
                        sql_statements.append(clean_statement)
                    is_collecting = False
                    current_statement = []
    return sql_statements

if __name__ == "__main__":
    sql_statements = extract_schema("test_databases/pagila/pagila-schema.sql")
    print("-- Pagila Database Schema")
    print("-- Essential Tables and Views\n")
    for stmt in sql_statements:
        print(stmt)
