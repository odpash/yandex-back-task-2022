import json

from aioflask import Blueprint
from flask import Response

from driveApp.db.Connection import Connection
blueprint = Blueprint('nodes_bl', __name__)


async def read_from_db(id):
    sql = f"""SELECT * FROM SystemItem WHERE id='{id}'"""
    connection = Connection(sql)
    res = await connection.select_all_command()
    res = dict(res[0])
    sizes = 0
    if res['type'] == "FOLDER":
        arr = []
        for c in json.loads(res['children']):
            size, el = await read_from_db(c)
            sizes += size
            arr.append(el)
        res['size'] = sizes
        res['children'] = arr
    else:
        sizes = res['size']
        res['children'] = None
    if res['url'] == 'null':
        res['url'] = None
    if res['parentid'] == 'null':
        res['parentid'] = None
    return sizes, res


@blueprint.route('/nodes/<id>', methods=['GET'])
async def handler(id):
    sql = f"""SELECT * FROM SystemItem WHERE id='{id}'"""
    connection = Connection(sql)
    res = await connection.select_all_command()
    if len(res) == 0:
        return Response(json.dumps({'code': 400, 'message': "Validation Failed!"}), 200, mimetype='application/json')
    _, res = await read_from_db(id)
    return Response(json.dumps(res).replace('parentid', "parentId"), 200, mimetype='application/json')
