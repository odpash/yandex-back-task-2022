from aioflask import Blueprint

blueprint = Blueprint('node_bl', __name__)


@blueprint.route('/node/<id>/history', methods=['GET'])
async def handler(id):
    return "node history"
