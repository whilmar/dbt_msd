%python
%pip install sqlglot

import json
import sqlglot
from sqlglot.expressions import Expression

# Example SQL query
file_path = "/Workspace/Users/petr.minar@merck.com/ast_test/study.sql"

try:
    with open(file_path, 'r') as file:
        content = file.read()
        sql_query = content.replace("`", "")
#        result = lineage(replaced_content)
except Exception as e:
    print(f"Error: {e}")

# Parse the SQL query to create an AST
ast = sqlglot.parse_one(sql_query)

def ast_to_dict(node):
    """
    Recursively convert AST node to a dictionary.
    """
    if not isinstance(node, Expression):
        return str(node)  # Convert non-serializable objects to strings

    result = {"type": node.__class__.__name__}
    for key, value in node.args.items():
        if isinstance(value, list):
            result[key] = [ast_to_dict(item) for item in value]
        elif isinstance(value, Expression):
            result[key] = ast_to_dict(value)
        else:
            result[key] = str(value)  # Convert non-serializable objects to strings

    return result

# Convert the AST to a dictionary
ast_dict = ast_to_dict(ast)

# Serialize the dictionary to JSON
ast_json = json.dumps(ast_dict, indent=2)
trimmed_json = ast_json.replace("\n","").replace("\t","").replace("  ","")
with open('/Workspace/Users/petr.minar@merck.com/output.txt', 'w') as file:
     file.write(trimmed_json)
print(ast_json)
