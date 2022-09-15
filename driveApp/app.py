import asyncio
from driveApp.api import apiCenter
from driveApp.db import schemas
from driveApp.db.Connection import Connection
from driveApp.secrets import POSTGRES_CONNECTION_SECRETS


async def prepare_database():
    connection = Connection(schemas.DATABASE_CHECK_CREATION_SQL)
    databases = await connection.select_all_command()   # Is db exists?
    exists = False
    for db in databases:
        if db['datname'] == POSTGRES_CONNECTION_SECRETS['database']:
            exists = True
            break
    if not exists:
        await connection.set_executable_string(schemas.DATABASE_CREATE_SQL)
        await connection.execute_command()  # Create Database
        await connection.set_executable_string(schemas.SCHEMA_CREATE_SQL)
        await connection.execute_command()  # Create Scheme

    await connection.set_executable_string(schemas.SYSTEM_ITEM_CREATE_SQL)
    await connection.execute_command()  # Create table SystemItem


def start_API():
    apiCenter.start_handlers()  # Execute handlers


def run():  # Entry point to the application
    loop = asyncio.get_event_loop()
    loop.run_until_complete(prepare_database())
    start_API()

