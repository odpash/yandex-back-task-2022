import asyncpg
from driveApp.secrets import POSTGRES_CONNECTION_SECRETS
from driveApp.db.schemas import DATABASE_CREATE_SQL

class Connection:
    def __init__(self, executable_string):
        self.__executable_string = executable_string
        self.__user = POSTGRES_CONNECTION_SECRETS['user']
        self.__password = POSTGRES_CONNECTION_SECRETS['password']
        self.__database = POSTGRES_CONNECTION_SECRETS['database']
        self.__host = POSTGRES_CONNECTION_SECRETS['host']
        self.__conn = None

    async def set_executable_string(self, s):
        self.__executable_string = s

    async def __connect(self):
        print(self.__user, self.__password, self.__database, self.__host)
        try:
            self.__conn = await asyncpg.connect(user=self.__user, password=self.__password, database=self.__database, host=self.__host)
        except asyncpg.InvalidCatalogNameError:
            self.__conn = await asyncpg.connect(user=self.__user, password=self.__password)

    async def __close_connection(self):
        await self.__conn.close()

    async def execute_command(self):
        print(self.__executable_string)
        await self.__connect()
        await self.__conn.execute(self.__executable_string)
        await self.__close_connection()

    async def select_all_command(self):
        await self.__connect()
        result_row = await self.__conn.fetch(self.__executable_string)
        await self.__close_connection()
        return result_row
