from src.services.database_service import DatabaseService
from src.services.pharmacy_service import PharmacyService

from flask import render_template
from flask.views import MethodView

class PharmacyOrders(MethodView, DatabaseService):
    def __init__(self, database_service):
        super().__init__()
        self.pharmacy_service = PharmacyService
        self.database_service = database_service

    def get(self):
        cur_order_query = f"SELECT order_id, date, patient_id FROM drug_order INNER JOIN pharmacy ON drug_order.pharmacy_id = pharmacy.UID WHERE order_status = 1 and pharmacy_id = {self.UID}"
        past_order_query = f"SELECT order_id, date, patient_id FROM drug_order INNER JOIN pharmacy ON drug_order.pharmacy_id = pharmacy.UID WHERE order_status = 0 and pharmacy_id = {self.UID}"
        cur_orders = self.pharmacy_service.fetch_all(query = cur_order_query)
        past_orders = self.pharmacy_service.fetch_all(query = past_order_query)

        cur_drug_list = []
        for i, ord in enumerate(cur_orders):
            cur_drug_list.append("")
            drug_query = f"SELECT drug_name FROM order_contains_drug NATURAL JOIN Drug WHERE order_id = {ord['order_id']}"
            drugs = self.pharmacy_service.fetch_all(query=drug_query)
            for drug in drugs:
                cur_drug_list[i] += drug["drug_name"] + ", "
        for i in range(len(cur_drug_list)):
            cur_drug_list[i] = cur_drug_list[i][:-2]

        past_drug_list = []
        for i, ord in enumerate(past_orders):
            past_drug_list.append("")
            drug_query = f"SELECT drug_name FROM order_contains_drug NATURAL JOIN Drug WHERE order_id = {ord['order_id']}"
            drugs = self.pharmacy_service.fetch_all(query=drug_query)
            for drug in drugs:
                past_drug_list[i] += drug["drug_name"] + ", "
        for i in range(len(past_drug_list)):
            past_drug_list[i] = past_drug_list[i][:-2]

        return render_template("pharmacy_orders.html", past_orders = past_orders, current_orders = cur_orders, current_drugs = cur_drug_list, past_drugs = past_drug_list)

    def post(self):
        return render_template("pharmacy_orders.html")