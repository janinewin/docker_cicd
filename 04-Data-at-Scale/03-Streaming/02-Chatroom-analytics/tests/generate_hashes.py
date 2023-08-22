import base64
import re
import pathlib

current_path = pathlib.Path(__file__).parent.absolute()
clickhouse_path = current_path.parent / "lwqueue" / "clickhouse_queries.py"
test_path = current_path / "test_all.py"


def generate_hash(query):
    encoded_bytes = base64.b64encode(query.encode("utf-8"))
    return encoded_bytes.decode("utf-8")


with open(clickhouse_path, "r") as f:
    content = f.read()
    queries = re.findall(
        r"# \$CHALLENGIFY_BEGIN\r?\n(.*?)# \$CHALLENGIFY_END", content, re.DOTALL
    )

    sql_keywords = ["SELECT", "WITH", "UPDATE", "INSERT", "DELETE"]
    queries = [
        query for query in queries if any(keyword in query for keyword in sql_keywords)
    ]

    queries = [
        re.sub(r"query\s*=\s*", "", query).replace('"""', "").strip()
        for query in queries
    ]

hashes = [generate_hash(query) for query in queries]

hash_names = ["correct_hash_1", "correct_hash_2", "correct_hash_3"]

with open(test_path, "r+") as f:
    content = f.read()
    for i, hash_name in enumerate(hash_names):
        hash_pattern = rf'({hash_name} = ")[\w\d]+(")'
        replacement = rf"\1{hashes[i]}\2"
        if re.search(hash_pattern, content):
            content = re.sub(hash_pattern, replacement, content)
        else:
            content += f'\n{hash_name} = "{hashes[i]}"\n'
    f.seek(0)
    f.write(content)
    f.truncate()
