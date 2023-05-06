from flask import Flask

from controllers import *

from src.containers.app_container import AppContainer

def create_app(app_container: AppContainer) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = app_container.config_service.secret_key

    app.add_url_rule("/pharmacy", view_func=PharmacyMain.as_view("pharmacy", database_service=app_container.database_service))

    return app

if __name__ == "__main__":
    app = create_app(app_container=AppContainer)
    app.run(host=AppContainer.config_service.host, port=AppContainer.config_service.port)
