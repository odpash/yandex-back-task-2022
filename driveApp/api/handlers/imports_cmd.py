from driveApp.api import validator
from driveApp.db.utils import importData
from aioflask import Blueprint, request, Response, jsonify
import json


blueprint = Blueprint('imports_bl', __name__)


@blueprint.route('/imports', methods=['POST'])
async def handler():
    request_params = request.json
    Validator = validator.ValidateSystemItemImport(request_params)
    validationResult = await Validator.check()
    if validationResult['code'] == 400:
        return Response(json.dumps(validationResult), status=validationResult['code'], mimetype='application/json')
    insertResult = await importData.uploadData(request_params)
    if not insertResult:
        return Response(json.dumps({"code": 400, "message": "Insert Failed!"}), status=400, mimetype='application/json')
    return Response(json.dumps({'code': 200, 'message': 'OK'}), status=200, mimetype='application/json')

