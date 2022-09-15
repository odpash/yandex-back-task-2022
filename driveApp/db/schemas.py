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
 children json
)"""
# # # # # # # # # # # # # # # # #


# Import handler Sql's
GET_ID_AND_PARENT_SQL = f"""SELECT (id, parentid, type) FROM SystemItem"""
UPDATE_BY_IDS_SQL = f"""update systemitem as t set -- postgres FTW
  url = n.url,
  parentId = n.parentId,
  size = n.size_,
  type = n.type_,
  date = n.date_
from (values
  insert_array
) as n(id, url, parentId, size_, type_, date_)
where n.id = t.id;"""


INSERT_NEW_ELEMENTS_SQL = f"""INSERT INTO SystemItem VALUES """
# # # # # # # # # # # # # # # # #