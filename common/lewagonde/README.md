# Le Wagon Data Engineering common functions

Library where we share common utilities.

## Functions

### `read_sql_query`

Wraps `pandas.read_sql_query` by creating a Postgres connection, executing `pandas.read_sql_query` and closing the connection.
