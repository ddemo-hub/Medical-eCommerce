from src.services.base_service import BaseService

from flask.views import MethodView

class PharmacyMain(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self):
        super().__init__()
        ...

    @BaseService.login_required
    def get(self):
        ...
        return ...