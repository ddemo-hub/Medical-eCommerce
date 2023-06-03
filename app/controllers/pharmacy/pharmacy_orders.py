from src.services.base_service import BaseService
from src.services.database_service import DatabaseService
from src.services.pharmacy_service import PharmacyService

from flask import render_template, request
from flask.views import MethodView


class PharmacyOrders(MethodView, BaseService, DatabaseService, PharmacyService):
    def __init__(self, database_service, pharmacy_service):
        super().__init__()
        self.pharmacy_service = pharmacy_service
        self.database_service = database_service

    @BaseService.login_required
    def get(self):
        cur_order_query = f"SELECT order_id, date, patient_id FROM drug_order INNER JOIN pharmacy ON drug_order.pharmacy_id = pharmacy.UID WHERE order_status = 1 and pharmacy_id = {self.uid}"
        past_order_query = f"SELECT order_id, date, patient_id FROM drug_order INNER JOIN pharmacy ON drug_order.pharmacy_id = pharmacy.UID WHERE order_status = 0 and pharmacy_id = {self.uid}"
        cur_orders = self.pharmacy_service.fetch_all(query=cur_order_query)
        past_orders = self.pharmacy_service.fetch_all(query=past_order_query)

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

        return render_template("pharmacy_orders.html", past_orders=past_orders, current_orders=cur_orders,
                               current_drugs=cur_drug_list, past_drugs=past_drug_list)

    def post(self):

        if "Complete" in request.form:
            order_id = request.form["order.id"]
            complete_query = f"UPDATE drug_orders SET order_status = 0 WHERE order_id = {order_id}"
            self.pharmacy_service.dml(complete_query)

        elif "Delete" in request.form:
            order_id = request.form["order_id"]
            delete_query = f"DELETE from drug_orders WHERE order_id = {order_id}"
            self.pharmacy_service.dml(delete_query)

        if "Home" in request.form:
            return render_template("pharmacy_main.html")
        #elif "ordermedicine" in request.form:
            #pass

        elif "editprofile" in request.form:
            return redirect(url_for("patient_edit"))
        elif "assistant" in request.form:
            return redirect(url_for('assistant'))
        elif "vieworders" in request.form:
            return redirect(url_for('patient_orders'))

        return render_template("pharmacy_orders.html")
