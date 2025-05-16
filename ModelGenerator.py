from app.db.connect import db
from peewee import *
import json, os


# imports for top of the model files
imports = """from peewee import *
from db import db
"""

# maps db types to peewee types, appart from VARCHAR which is handled separately in the map_type function
type_map = {
    'INTEGER': 'IntegerField',
    'TEXT': 'TextField',
    'REAL': 'FloatField',
    'BLOB': 'BlobField',
    'NUMERIC': 'DecimalField',
    'DATE': 'DateField',
    'DATETIME': 'DateTimeField',
}

def map_type(db_type: str) -> str:
    """
    Map SQLite type to Peewee type.
    """

    if db_type.startswith('VARCHAR'):
        return 'CharField'
    else:
        return type_map.get(db_type, 'TextField')

def snake_case_to_pascal_case(text: str) -> str:
    """
    Convert snake_case string to PascalCase.
    """
    return ''.join(word.capitalize() for word in text.split('_'))

def snake_case_to_camel_case(text: str) -> str:
    """
    Convert snake_case string to camelCase.
    """
    words = text.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

def generate_models() -> dict[str, str]:
    db.connect()

    cursor = db.execute_sql('SELECT name FROM sqlite_master WHERE type="table";')

    table_names = [row[0] for row in cursor.fetchall()]
    table_names.remove("sqlite_sequence")  # remove the sqlite_sequence table

    # dict of model file names to their contents
    model_files = {}

    for name in table_names:
        camel_name = snake_case_to_camel_case(name)
        pascal_name = snake_case_to_pascal_case(name)

        cursor.execute(f"PRAGMA table_info({name});")
        columns = cursor.fetchall()

        model_files[camel_name] = f"{imports}\nclass {pascal_name}(Model):\n"
        
        for column in columns:
            model_files[camel_name] += f"    {snake_case_to_camel_case(column[1])} = {map_type(column[2])}()\n"

        model_files[camel_name] += f"\n"
        model_files[camel_name] += f"    class Meta:\n"
        model_files[camel_name] += f"        database = db\n"
    return model_files

def write_models_to_directory(models: dict[str, str], dir_path: str) -> None:
    
    # check if the directory exists, and create it if it doesn't
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for file_name, content in models.items():
        with open(f"{dir_path}/{file_name}.py", "w") as f:
            f.write(content)
            print(f"Generated model file: {file_name}.py")
    pass

if __name__ == "__main__":
    models = generate_models()
    write_models_to_directory(models, "ModelGeneratorTesting")
    # print(json.dumps(models, indent=4))
    pass