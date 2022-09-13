from aioflask import Blueprint

blueprint = Blueprint('delete_bl', __name__)


@blueprint.route('/delete/<id>', methods=['DELETE'])
async def handler():
    return "delete"
