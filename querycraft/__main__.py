from querycraft.utils.db_connector import DatabaseConnector

def main():
    schema_name = input("Enter the schema name (e.g., fruitmart, pagila-hw): ").strip()
    db = DatabaseConnector(schema_name=schema_name)
    db.interactive_mode()

if __name__ == "__main__":
    main()
