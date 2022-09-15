from aioflask import Blueprint, request, Response
import json
from driveApp.api.validators.SystemItemImportValidator import SystemItemImportValidator
from driveApp.db.Connection import Connection
from driveApp.db.schemas import GET_ID_AND_PARENT_SQL


async def get_information_from_db():
    connection = Connection(GET_ID_AND_PARENT_SQL)
    data = await connection.select_all_command()
    return data

blueprint = Blueprint('imports_bl', __name__)


@blueprint.route('/imports', methods=['POST'])
async def handler():
    data = await get_information_from_db()
    request_params = request.json
    validator = SystemItemImportValidator(request_params, data)
    validationResult = await validator.check()
    if validationResult['code'] == 400:
        return Response(json.dumps(validationResult), status=validationResult['code'], mimetype='application/json')
    #insertResult = await importData.uploadData(request_params)
    insertResult = False
    if not insertResult:
        return Response(json.dumps({"code": 400, "message": "Insert Failed!"}), status=400, mimetype='application/json')
    return Response(json.dumps({'code': 200, 'message': 'OK'}), status=200, mimetype='application/json')

