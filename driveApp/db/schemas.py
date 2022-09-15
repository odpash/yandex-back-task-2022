import asyncio
from driveApp.secrets import POSTGRES_CONNECTION_SECRETS


# DATABASE create
DATABASE_CHECK_CREATION_SQL = f"""SELECT * FROM pg_catalog.pg_database"""
DATABASE_CREATE_SQL = f"CREATE DATABASE {POSTGRES_CONNECTION_SECRETS['database']}"
SCHEMA_CREATE_SQL = f"CREATE SCHEMA {POSTGRES_CONNECTION_SECRETS['database']}"
# # # # # # # # # # # # # # # # #

# Tables create
SYSTEM_ITEM_CREATE_SQL = """CREATE TABLE IF NOT EXISTS SystemItem(
id text NOT NULL,
url text,
date text NOT NULL, 
parentId text,
type text, 
size integer,
 children text
)"""
# # # # # # # # # # # # # # # # #


# Import handler Sql's
GET_ID_AND_PARENT_SQL = f"""SELECT (id, parentid, type, children) FROM SystemItem"""
INSERT_NEW_FILE_SQL = f"""INSERT INTO SystemItem (id, url, date, parentid, type, size, children) VALUES """
INSERT_NEW_FOLDER_SQL = f"""INSERT INTO SystemItem (id, date, parentid, type, children) VALUES """
# # # # # # # # # # # # # # # # #