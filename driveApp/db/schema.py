import asyncio


systemItem = """CREATE TABLE IF NOT EXISTS SystemItem(
id text NOT NULL,
url text,
date text NOT NULL,
parentId text,
type text, 
size integer,
 children json
)"""

