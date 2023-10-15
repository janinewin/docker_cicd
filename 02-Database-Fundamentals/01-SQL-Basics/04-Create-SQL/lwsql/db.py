from lwsql.btree import DiskBTree
from lwsql.parser import SQLParser


class DB:
    def __init__(self, filename, t=2):
        self.filename = filename
        self.btree = DiskBTree(t, filename)
        self.sql_parser = SQLParser()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @staticmethod
    def map_data_type(data_type_str):
        if data_type_str == "int":
            return int
        elif data_type_str == "str":
            return str
        else:
            raise ValueError(f"Invalid data type: {data_type_str}")

    def execute_sql(self, sql):
        parsed_sql = self.sql_parser.parse(sql)
        if parsed_sql is None:
            raise Exception(f"Invalid SQL statement: {sql}")

        if parsed_sql[0] == "CREATE TABLE":
            table_name = parsed_sql[1]
            schema = {}
            for i in range(2, len(parsed_sql)):
                column = parsed_sql[i]
                data_type_str = column[1]
                data_type = self.map_data_type(data_type_str)
                schema[column[0]] = data_type
            metadata = self.btree.read_metadata()
            if table_name in metadata["tables"]:
                raise Exception(f"Table {table_name} already exists.")
            self.btree.select_table(table_name, schema)

        elif parsed_sql[0] == "INSERT INTO":
            pass  # YOUR CODE HERE

        elif parsed_sql[0] == "SELECT":
            pass  # YOUR CODE HERE

        else:
            raise Exception(f"Invalid SQL statement: {sql}")

    def close(self):
        self.btree.close()
