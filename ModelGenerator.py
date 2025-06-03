from gallery.db.connect import db
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
            col_name_camel = snake_case_to_camel_case(column[1])
            col_type = map_type(column[2])
            
            # check if column is a foreign key
            cursor.execute(f"PRAGMA foreign_key_list({name});")
            foreign_keys = cursor.fetchall()
            
            is_foreign_key = False
            for fk in foreign_keys:
                if column[1] == fk[3]:  # 3 is the 'from' column
                    is_foreign_key = True
                    referenced_table_pascal = snake_case_to_pascal_case(fk[2]) # 2 is the 'table' column
                    model_files[camel_name] += f"    {col_name_camel} = ForeignKeyField({referenced_table_pascal}, backref='{name}')\n"
                    break
            
            if not is_foreign_key:
                model_files[camel_name] += f"    {col_name_camel} = {col_type}()\n"

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
    
    # generate __init__.py file
    generate_init_file(models, dir_path)

def generate_init_file(models: dict[str, str], dir_path: str) -> None:
    """
    Generate __init__.py file to make the directory a proper Python package.
    """
    
    # extract class names from the models
    class_names = []
    file_names = []
    
    for file_name, content in models.items():
        file_names.append(file_name)
        # extract class name from the model content (find class definition)
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('class '):
                class_name = line.split('class ')[1].split('(')[0].strip()
                class_names.append(class_name)
                break
    
    # create the __init__.py content
    init_content = '"""\nGenerated models from database schema.\n"""\n\n'
    
    # add imports
    init_content += "# import all model classes\n"
    for i, file_name in enumerate(file_names):
        class_name = class_names[i]
        init_content += f"from .{file_name} import {class_name}\n"
    
    # add __all__ list
    init_content += "\n# expose all classes for external imports\n"
    init_content += "__all__ = [\n"
    for class_name in class_names:
        init_content += f'    "{class_name}",\n'
    init_content += "]\n"
    
    # write the __init__.py file
    with open(f"{dir_path}/__init__.py", "w") as f:
        f.write(init_content)
        print(f"Generated __init__.py file")

if __name__ == "__main__":
    models = generate_models()
    write_models_to_directory(models, "app/ModelGeneratorTesting")
    # print(json.dumps(models, indent=4))
    pass