from src.services.base_service import BaseService
from src.services.database_service import DatabaseService

from flask.views import MethodView
from flask import render_template

class PharmacyMain(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service: DatabaseService):
        super().__init__()
        self.database_service = database_service
        ###############################
        self.uid = 2
        self.name = "bilkent eczanesi"
        ###############################

    #@BaseService.login_required
    def get(self):
        count_waiting_orders = f"SELECT COUNT(*) as count FROM Drug_Order " +\
                               f"WHERE pharmacy_id = {self.uid} AND order_status = 'pending approval'"

        order_count = self.database_service.dql(query=count_waiting_orders, columns=["count"])["count"][0]

        return render_template("pharmacy/pharmacy_main.html", name=self.name, order_count=order_count)
