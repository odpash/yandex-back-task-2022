import asyncpg


async def connect():
    conn = await asyncpg.connect(user='postgres', password='991155',
                                 database='spok', host='127.0.0.1')
    return conn


async def execute_command(executable_string):
    conn = await connect()
    await conn.execute(executable_string)
    await conn.close()
