from driveApp.db.utils.Connection import execute_command
from .. import schema


async def create_tables():
    await execute_command(schema.systemItem)


