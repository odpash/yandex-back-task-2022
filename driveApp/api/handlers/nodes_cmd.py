from aioflask import Blueprint

blueprint = Blueprint('nodes_bl', __name__)


@blueprint.route('/nodes/<id>', methods=['GET'])
async def handler(id):
    return "nodes"
