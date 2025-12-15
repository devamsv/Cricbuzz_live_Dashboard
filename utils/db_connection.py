import mysql.connector
from mysql.connector import Error
import pandas as pd


def create_connection(host, user, passwd, database=None, port=None):
    """Create a new MySQL connection. Don't cache connections across reruns.

    If `host` is empty or the Windows named-pipe shorthand ("."), prefer TCP
    by using the loopback address `127.0.0.1`. An optional `port` can be
    provided (defaults to server's configured port, typically 3306).
    """
    # On Windows a host value of '.' attempts a named-pipe connection which
    # may fail with: "Can't open named pipe to host: . pipe: MySQL (2)".
    if host in (None, "", "."):
        host = "127.0.0.1"

    connect_kwargs = {
        "host": host,
        "user": user,
        "password": passwd,
        "database": database,
        "autocommit": True,
    }
    if port:
        try:
            connect_kwargs["port"] = int(port)
        except Exception:
            pass

    return mysql.connector.connect(**{k: v for k, v in connect_kwargs.items() if v is not None})


def get_mysql_schema(host, user, passwd):
    """
    Returns a nested dict of available user databases, their tables, and columns.
    Excludes system databases.
    """
    conn = create_connection(host, user, passwd)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    all_databases = [db[0] for db in cursor]

    excluded_dbs = {"information_schema", "performance_schema", "mysql", "sys"}
    full_schema_info = {}

    for db_name in all_databases:
        if db_name in excluded_dbs:
            continue

        try:
            db_conn = create_connection(host, user, passwd, db_name)
            db_cursor = db_conn.cursor()
            
            db_cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
            tables = db_cursor.fetchall()
            if not tables:
                continue

            db_structure = {"tables": {}, "views": {}, "functions": {}, "procedures": {}}

            for row in tables:
                tbl = row[0]
                col_q = """
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                    ORDER BY ORDINAL_POSITION
                """
                db_cursor.execute(col_q, (db_name, tbl))
                cols = db_cursor.fetchall()
                db_structure["tables"][tbl] = [
                    {
                        "name": c[0],
                        "type": c[1],
                        "nullable": c[2],
                        "key": c[3],
                        "default": c[4],
                        "extra": c[5],
                    }
                    for c in cols
                ]

            # Views
            db_cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
            views = db_cursor.fetchall()
            for v in views:
                db_structure["views"][v[0]] = {}

            full_schema_info[db_name] = db_structure

            db_cursor.close()
            db_conn.close()
        except Error:
            continue

    cursor.close()
    conn.close()
    return full_schema_info


def list_databases(host, user, passwd):
    schema = get_mysql_schema(host, user, passwd)
    return sorted(list(schema.keys()))


def list_tables(host, user, passwd, database):
    schema = get_mysql_schema(host, user, passwd)
    if database not in schema:
        return []
    return sorted(list(schema[database]["tables"].keys()))


def get_table_columns(host, user, passwd, database, table):
    schema = get_mysql_schema(host, user, passwd)
    return schema.get(database, {}).get("tables", {}).get(table, [])


def fetch_table(host, user, passwd, database, table, limit=200):
    """Return dataframe and the exact SQL used."""
    conn = create_connection(host, user, passwd, database)
    sql = f"SELECT * FROM `{table}` LIMIT {int(limit)};"
    df = pd.read_sql(sql, conn)
    conn.close()
    return df, sql


def run_select(host, user, passwd, database, select_sql):
    """Run a user-provided SELECT (read-only)."""
    if not select_sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed here.")
    conn = create_connection(host, user, passwd, database)
    df = pd.read_sql(select_sql, conn)
    conn.close()
    return df


def insert_row(host, user, passwd, database, table, data):
    """Insert a row using parameterized SQL. Returns affected rows and SQL preview."""
    cols = [f"`{c}`" for c in data.keys()]
    placeholders = ", ".join(["%s"] * len(cols))
    sql = f"INSERT INTO `{table}` ({', '.join(cols)}) VALUES ({placeholders});"
    values = list(data.values())

    conn = create_connection(host, user, passwd, database)
    cur = conn.cursor()
    cur.execute(sql, values)
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected, sql


def delete_rows(host, user, passwd, database, table, where_clause):
    """Delete rows matching a WHERE clause. (Use carefully.)"""
    where = where_clause.strip()
    if not where:
        raise ValueError("Refusing to delete without a WHERE clause.")
    sql = f"DELETE FROM `{table}` WHERE {where};"
    conn = create_connection(host, user, passwd, database)
    cur = conn.cursor()
    cur.execute(sql)
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected, sql


def execute_update(host, user, passwd, database, table, set_clause, where_clause):
    """Run an UPDATE with user-provided SET and WHERE parts."""
    set_part = set_clause.strip()
    where_part = where_clause.strip()
    if not set_part:
        raise ValueError("SET clause cannot be empty.")
    if not where_part:
        raise ValueError("Refusing to update without a WHERE clause.")
    sql = f"UPDATE `{table}` SET {set_part} WHERE {where_part};"
    conn = create_connection(host, user, passwd, database)
    cur = conn.cursor()
    cur.execute(sql)
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected, sql
