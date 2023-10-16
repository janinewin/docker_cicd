import os
import pickle

METADATA_SIZE = 4096


class Node:
    def __init__(self, leaf=True):
        """
        Initialize a node in the BTree.

        Parameters:
            leaf (bool): Whether the node is a leaf node (default is True).
        """
        self.leaf = leaf
        self.keys = []
        self.child_offsets = []
        self.rows = []


class DiskBTree:
    def __init__(self, t, filename):
        """
        Initialize a Disk-based BTree object.

        Parameters:
            t (int): The minimum degree of the BTree.
            filename (str): The name of the file where data will be stored.
        """
        self.t = t
        self.filename = filename
        self.root_offset = None
        self.table_name = None
        self.schema = {}
        if os.path.exists(self.filename):
            self.file = open(self.filename, "rb+")
        else:
            self.file = open(self.filename, "wb+")
            self.write_metadata({"tables": {}})

    def select_table(self, table_name, schema=None):
        """
        Selects the table to perform operations on.

        Parameters:
            table_name (str): The name of the table to select.
            schema (dict): Optional schema describing column data types (default is None).
        """
        self.table_name = table_name
        metadata = self.read_metadata()
        if table_name in metadata["tables"]:
            self.root_offset = metadata["tables"][table_name]["root_offset"]
            self.schema = metadata["tables"][table_name].get("schema", {})
        else:
            if schema is None:
                raise ValueError("Schema must be provided for new tables.")
            self.schema = schema
            root = Node()
            self.root_offset = self.write_node(root)
            self.update_metadata_with_schema()

    def update_metadata_with_schema(self):
        """
        Updates metadata on the disk with the current root_offset and schema.
        """
        metadata = self.read_metadata()
        metadata["tables"][self.table_name] = {
            "root_offset": self.root_offset,
            "schema": self.schema,
        }
        self.write_metadata(metadata)

    def write_metadata(self, metadata):
        """
        Writes metadata to the disk.

        Parameters:
            metadata (dict): The metadata to write.
        """
        self.file.seek(0)
        packed_data = pickle.dumps(metadata)
        if len(packed_data) > METADATA_SIZE:
            raise ValueError("Metadata size exceeds reserved space.")
        self.file.write(packed_data)
        self.file.write(b" " * (METADATA_SIZE - len(packed_data)))  # Padding
        self.file.flush()

    def read_metadata(self):
        """
        Reads metadata from the disk.

        Returns:
            dict: The read metadata.
        """
        self.file.seek(0)
        packed_data = self.file.read(METADATA_SIZE).rstrip(b" ")  # Remove padding
        return pickle.loads(packed_data)

    def insert_non_full(self, x, k, row_data):
        """
        Inserts a key-value pair into a non-full node.

        Parameters:
            x (Node): The node to insert into.
            k (int): The key to insert.
            row_data (dict): The corresponding row data.
        """
        if x.leaf:
            x.keys.append(k)
            x.rows.append(row_data)
            sorted_keys_rows = sorted(zip(x.keys, x.rows))
            x.keys, x.rows = zip(*sorted_keys_rows)
            x.keys = list(x.keys)
            x.rows = list(x.rows)
        else:
            i = len(x.keys) - 1
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            child = self.read_node(x.child_offsets[i])
            if len(child.keys) == (2 * self.t) - 1:
                self.split(x, i)
                if k > x.keys[i]:
                    i += 1
                    child = self.read_node(x.child_offsets[i])
            self.insert_non_full(child, k, row_data)
            self.write_node(child)

    def write_node(self, node):
        """
        Writes a node to the disk.

        Parameters:
            node (Node): The node to write.

        Returns:
            int: The disk offset where the node was written.
        """
        self.file.seek(0, 2)
        offset = self.file.tell()
        pickle.dump(node, self.file)
        self.file.flush()
        return offset

    def split(self, parent, i):
        """
        Splits a full child node.

        Parameters:
            parent (Node): The parent node.
            i (int): The index of the child to split in parent's child_offsets.
        """
        child = self.read_node(parent.child_offsets[i])
        new_child = Node(leaf=child.leaf)

        middle_key = child.keys[self.t - 1]
        middle_row = child.rows[self.t - 1]
        parent.keys.insert(i, middle_key)
        parent.rows.insert(i, middle_row)
        parent.child_offsets.insert(i + 1, self.write_node(new_child))

        new_child.keys = child.keys[self.t :]
        new_child.rows = child.rows[self.t :]
        child.keys = child.keys[: self.t - 1]
        child.rows = child.rows[: self.t - 1]

        if not child.leaf:
            new_child.child_offsets = child.child_offsets[self.t :]
            child.child_offsets = child.child_offsets[: self.t]

        self.write_node(child)
        self.write_node(new_child)

    def read_node(self, offset):
        """
        Reads a node from the disk.

        Parameters:
            offset (int): The disk offset where the node is stored.

        Returns:
            Node: The read node.
        """
        self.file.seek(offset)
        return pickle.load(self.file)

    def search(self, k):
        """
        Searches for a key in the BTree.

        Parameters:
            k (int): The key to search for.

        Returns:
            dict: The row data corresponding to the key, or None if not found.
        """
        x_offset = self.root_offset
        x = self.read_node(x_offset)

        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1

        if i < len(x.keys) and k == x.keys[i]:
            return x.rows[i]

        if x.leaf:
            return None

        return self.search(k, x.child_offsets[i])

    def insert(self, key, row_data):
        """
        Inserts a key-value pair into the BTree.

        Parameters:
            key (int): The key to insert.
            row_data (dict): The corresponding row data.
        """
        if self.schema:
            for column, data_type in self.schema.items():
                if column not in row_data or not isinstance(
                    row_data[column], data_type
                ):
                    raise ValueError(
                        f"Invalid data for column {column}. Expected type {data_type}."
                    )

        root = self.read_node(self.root_offset)
        if len(root.keys) == (2 * self.t) - 1:
            temp = Node()
            temp.child_offsets.append(self.root_offset)
            self.split(temp, 0)
            self.insert_non_full(temp, key, row_data)
            self.root_offset = self.write_node(temp)
            self.update_metadata_with_schema()
        else:
            self.insert_non_full(root, key, row_data)
            self.root_offset = self.write_node(root)
            self.update_metadata_with_schema()

    def close(self):
        """
        Closes the disk file.
        """
        self.file.close()
