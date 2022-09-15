import json

from aioflask import Blueprint
from flask import Response, request

from driveApp.db.Connection import Connection
from driveApp.db.schemas import GET_ID_AND_PARENT_SQL

blueprint = Blueprint('delete_bl', __name__)


async def getInformationFromDb() -> list:
    connection = Connection(GET_ID_AND_PARENT_SQL)
    data = await connection.select_all_command()
    for i in range(len(data)):
        data[i] = list(data[i])[0]
        data[i] = list(data[i])
        data[i][3] = json.loads(data[i][3])
        data[i] = tuple(data[i])
    return data


async def updateTree(id, dbData, arr):
    for i in range(len(dbData)):
        if dbData[i][0] == id:
            arr.append(dbData[i][0])
            for c in dbData[i][3]:
                await updateTree(c, dbData, arr)
            break
    return arr


async def writeData(arr):
    connection = Connection("""""")
    for i in arr:
        sql = f"""DELETE FROM SystemItem WHERE id='{i}'"""
        await connection.set_executable_string(sql)
        await connection.execute_command()


@blueprint.route('/delete/<id>', methods=['DELETE'])
async def handler(id):
    dbData = await getInformationFromDb()
    is_inside = False
    # TODO: add 400 error
    for i in dbData:
        if i[0] == id:
            is_inside = True
    if not is_inside:
        return Response(json.dumps({'code': 404, 'message': 'Item not found'}), 404, mimetype='application/json')
    arr_to_update = []
    arr_to_update = await updateTree(id, dbData, arr_to_update)
    await writeData(arr_to_update)
    return Response(json.dumps({'code': 200, 'message': "Ok"}), 200, mimetype='application/json')
