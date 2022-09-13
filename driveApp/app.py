import asyncio
from driveApp.api import apiCenter
from driveApp.db.utils import initialize_db


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_db.create_tables())
    loop.run_until_complete(apiCenter.start_handlers())

