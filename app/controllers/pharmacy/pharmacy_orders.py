from src.services.database_service import DatabaseService
from src.services.pharmacy_service import PharmacyService
from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class PharmacyOrders(MethodView, BaseService):
    def __init__(self, database_service, pharmacy_service):
        super().__init__()
        self.pharmacy_service = pharmacy_service
        self.database_service = database_service

    @BaseService.login_required
    def get(self):
        name = self.name

        cur_order_query = f"SELECT order_id, date, patient_id FROM drug_order INNER JOIN pharmacy ON " \
                          f"drug_order.pharmacy_id = pharmacy.UID WHERE order_status = 1 and pharmacy_id = {self.uid}"

        past_order_query = f"SELECT order_id, date, patient_id FROM drug_order INNER JOIN pharmacy ON " \
                           f"drug_order.pharmacy_id = pharmacy.UID WHERE order_status = 0 and pharmacy_id = {self.uid}"
        cur_orders = self.pharmacy_service.fetch_all(query = cur_order_query)
        past_orders = self.pharmacy_service.fetch_all(query = past_order_query)

        cur_drug_list = []
        for i, ords in enumerate(cur_orders):
            cur_drug_list.append("")
            drug_query = f"SELECT drug_name FROM order_contains_drug NATURAL JOIN Drug WHERE order_id = {ords['order_id']}"
            drugs = self.pharmacy_service.fetch_all(query=drug_query)
            for drug in drugs:
                cur_drug_list[i] += drug["drug_name"] + ", "
        for i in range(len(cur_drug_list)):
            cur_drug_list[i] = cur_drug_list[i][:-2]

        past_drug_list = []
        for i, ords in enumerate(past_orders):
            past_drug_list.append("")
            drug_query = f"SELECT drug_name FROM order_contains_drug NATURAL JOIN Drug WHERE order_id = {ords['order_id']}"
            drugs = self.pharmacy_service.fetch_all(query=drug_query)
            for drug in drugs:
                past_drug_list[i] += drug["drug_name"] + ", "
        for i in range(len(past_drug_list)):
            past_drug_list[i] = past_drug_list[i][:-2]


        return render_template("pharmacy/pharmacy_orders.html", name = name, past_orders = past_orders, current_orders = cur_orders, current_drugs = cur_drug_list, past_drugs = past_drug_list)

    def post(self):
        message = ''

        if "Home" in request.form:
            return redirect(url_for('pharmacy_main'))

        if "Complete" in request.form:
            order_id = request.form.get("Complete")
            complete_query = f"UPDATE Drug_Order SET order_status = 0 WHERE order_id = {order_id}"
            self.database_service.dml(complete_query)
            return redirect(url_for("pharmacy_orders"))

        if "viewreport" in request.form:
            return redirect(url_for("pharmacy_report"))

        if "logout" in request.form:
            session.clear()
            session["uid"] = None
            session["logged_in"] = False
            return redirect(url_for('login'))