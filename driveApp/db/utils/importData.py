from driveApp.db.utils.Connection import connect


async def is_folder_db(parentId):
    conn = await connect()
    row = await conn.fetchrow(
        'SELECT * FROM systemitem WHERE parentId = $1', parentId)
    return row


async def uploadData(data):
    conn = await connect()

