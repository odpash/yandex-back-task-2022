from aioflask import Blueprint

blueprint = Blueprint('updates_bl', __name__)


@blueprint.route('/updates', methods=['GET'])
async def handler():
    return "updates"
