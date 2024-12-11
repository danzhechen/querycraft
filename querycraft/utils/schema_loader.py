import yaml
from pathlib import Path
from typing import Optional

class SchemaLoader:
    def __init__(self, schema_name: Optional[str] = None):
        """Initialize SchemaLoader without a default schema
        
        Args:
            schema_name (str, optional): Name of the schema to load
        
        Raises:
            ValueError: If no schema_name is provided and no default can be determined
        """
        self.base_path = Path("querycraft/schemas")
        if schema_name:
            self.schema_dir = self.base_path / schema_name
            self.sql_path = self.schema_dir / f"{schema_name}.sql"
            self.yaml_path = self.schema_dir / f"{schema_name}.yaml"

        if schema_name is None:
            available_schemas = self.list_available_schemas()
            if not available_schemas:
                raise ValueError("No schema files found in querycraft/schemas/")
            raise ValueError("Schema name must be provided. Available schemas: "
                           f"{', '.join(available_schemas)}")
        
        self.schema_name = schema_name

    def load_schema(self, schema_path: Optional[str] = None) -> str:
        """Load the raw SQL schema"""
        path_to_use = Path(schema_path) if schema_path else self.sql_path
        if not path_to_use.exists():
            available = self.list_available_schemas()
            raise FileNotFoundError(
                f"Schema file not found: {path_to_use}\n"
                f"Available schemas: {', '.join(available)}"
            )

        with open(path_to_use, 'r') as f:
            return f.read()

    def get_examples(self) -> str:
        """Get example queries from the YAML file"""
        if not self.yaml_path.exists():
            return "No example queries available."
            
        with open(self.yaml_path, 'r') as f:
            examples_data = yaml.safe_load(f)
            
        if not examples_data or 'example_queries' not in examples_data:
            return "No example queries available."
        
        examples = []
        for ex in examples_data['example_queries']:
            examples.append(f"Question: {ex['question']}\nSQL: {ex['sql']}\n")
        
        return "\n".join(examples)

    @classmethod
    def list_available_schemas(cls) -> list:
        """List all available schema files"""
        schema_dir = Path("querycraft/schemas")
        return [d.name for d in schema_dir.iterdir()
                if d.is_dir() and (d / f"{d.name}.sql").exists()]
