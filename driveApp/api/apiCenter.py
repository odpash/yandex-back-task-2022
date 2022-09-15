from aioflask import Flask
from driveApp.api.handlers import imports_cmd, delete_cmd, nodes_cmd, updates_cmd, node_cmd


def start_handlers():
    """
    INITIALIZE Handlers
    :return:
    """
    app.register_blueprint(imports_cmd.blueprint)
    app.register_blueprint(delete_cmd.blueprint)
    app.register_blueprint(nodes_cmd.blueprint)
    app.register_blueprint(updates_cmd.blueprint)
    app.register_blueprint(node_cmd.blueprint)
    app.run(port=8080)


app = Flask(__name__)
