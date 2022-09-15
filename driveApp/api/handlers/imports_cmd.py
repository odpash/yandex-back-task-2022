import logging

from aioflask import Blueprint, request, Response
import json
from driveApp.api.validators.SystemItemImportValidator import SystemItemImportValidator
from driveApp.db.Connection import Connection
from driveApp.db.schemas import GET_ID_AND_PARENT_SQL, INSERT_NEW_FILE_SQL, INSERT_NEW_FOLDER_SQL


async def updateTree(dbData, element, arr):
    for i in range(len(dbData)):  # if element is new
        dbData[i] = tuple(dbData[i])
        if element['parentId'] == dbData[i][0]:
            dbData[i][3].append(element['id'])
            dbData[i] = tuple(dbData[i])
            arr.append(dbData[i])
    return arr


async def changeToNull(dbData, element, arr):
    if type(element) == dict:
        element_id = element['id']
    else:
        element_id = element[0]
    for i in range(len(dbData)):
        dbData[i] = list(dbData[i])
        if element_id in dbData[i][3]:
            dbData[i][1] = None
            dbData[i] = tuple(dbData[i])
            arr.append(dbData[i])
            for j in dbData[3]:
                await changeToNull(dbData, j, arr)
    return arr

    # if element больше не ребенок


async def moreNotaChild(dbData, element, arr):
    for i in range(len(dbData)):
        dbData[i] = list(dbData[i])
        if element['id'] in dbData[i][3]:
            dbData[i][3].pop(element['id'])
            dbData[i] = tuple(dbData[i])
            arr.append(dbData[i])
    return arr


async def prepareToUpdateDb(dbData: list, newData: dict) -> (list, list, list, str):
    toInsert, toUpdate, toUpdateParent, date = [], [], [], newData['updateDate']
    print(newData['items'], "NEWEL")
    for newElement in newData['items']:
        is_new = True
        for oldElement in dbData:
            if newElement['id'] == oldElement[0]:  # если элемент уже есть в базе
                is_new = False
                # if newElement['parentId'] is None:  # если он стал корневым
                #     toUpdateParent = await changeToNull(dbData, newElement, toUpdateParent)
                #     print(toUpdateParent, "CHANGE TO NULL")
                # if newElement['parentId'] != oldElement[1]:
                #     toUpdateParent = await moreNotaChild(dbData, newElement, toUpdateParent)
                #     print(toUpdateParent, "MoreNotAChild")
        newElement['date'] = newData['updateDate']
        if is_new:
            toUpdateParent = await updateTree(dbData, newElement, toUpdateParent)
            print(toUpdateParent, "NEW ELEMENT")
            toInsert.append(newElement)
        else:
            toUpdate.append(newElement)
    return toInsert, toUpdate, toUpdateParent, date


async def getInformationFromDb() -> list:
    connection = Connection(GET_ID_AND_PARENT_SQL)
    data = await connection.select_all_command()
    for i in range(len(data)):
        data[i] = list(data[i])[0]
        data[i] = list(data[i])
        data[i][3] = json.loads(data[i][3])
        data[i] = tuple(data[i])
    return data


async def writeToDb(toInsert, toUpdate, toUpdateParent, date):
    connection = Connection(INSERT_NEW_FILE_SQL)
    print(toUpdateParent)
    for i in toInsert:

        if i['type'] == 'FILE':
            d = (i['id'], i['url'], i['date'], str(i['parentId']), i['type'], i['size'], "[]")
            await connection.set_executable_string(INSERT_NEW_FILE_SQL + str(d).replace('None', 'null'))
        else:
            d = (i['id'], i['date'], i['parentId'], i['type'], "[]")
            await connection.set_executable_string(INSERT_NEW_FOLDER_SQL + str(d).replace('None', 'null'))

        await connection.execute_command()

    for i in toUpdate:
        if i['type'] == 'FILE':
            sql = f"""UPDATE SystemItem SET url='{str(i['url'])}', date='{i['date']}', parentid='{str(i['parentId'])}', type='{i['type']}', size={i['size']} WHERE id='{i['id']}'"""

        else:
            sql = f"""UPDATE SystemItem SET date='{i['date']}', parentid='{str(i['parentId'])}', type='{i['type']}' WHERE id='{i['id']}'"""

        await connection.set_executable_string(sql.replace('None', 'null'))
        await connection.execute_command()

    for i in toUpdateParent:
        sql = f"""UPDATE SystemItem SET parentid='{str(i[1])}', date='{date}', children='{str(json.dumps(i[3]))}', type='{str(i[2])}' WHERE id='{i[0]}'"""
        await connection.set_executable_string(sql.replace('None', 'null'))
        await connection.execute_command()


blueprint = Blueprint('imports_bl', __name__)


@blueprint.route('/imports', methods=['POST'])
async def handler():
    data = await getInformationFromDb()
    data_c = list(data)
    request_params = request.json
    validator = SystemItemImportValidator(request_params, data_c)
    validationResult = await validator.check()
    if validationResult['code'] == 400:
        return Response(json.dumps(validationResult), status=validationResult['code'], mimetype='application/json')
    logging.info("Validation Complete!")
    toInsert, toUpdate, toUpdateParent, date = await prepareToUpdateDb(data, request_params)
    try:
        await writeToDb(toInsert, toUpdate, toUpdateParent, date)
    except Exception as e:
        print("WRITE ERROR!", e)
    # insertResult = await importData.uploadData(request_params)
    insertResult = True
    if not insertResult:
        return Response(json.dumps({"code": 400, "message": "Insert Failed!"}), status=400, mimetype='application/json')
    return Response(json.dumps({'code': 200, 'message': 'OK'}), status=200, mimetype='application/json')
