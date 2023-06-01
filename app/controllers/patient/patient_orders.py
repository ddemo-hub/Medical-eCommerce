from src.services.base_service import BaseService
from flask.views import MethodView
from flask import render_template, request, redirect, url_for

class PatientOrders(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, patient_service):
        super().__init__()
        self.database_service = database_service
        self.patient_service = patient_service
    
    @BaseService.login_required
    def get(self):
        balance_query = f"SELECT Wallet_balance FROM Patient " +\
                               f"WHERE UID = {self.uid}"
        
        balance = self.patient_service.fetch_one(query=balance_query)
        
        name_query = f"SELECT name FROM User " +\
                               f"WHERE UID = {self.uid}"
        name = self.patient_service.fetch_one(query=name_query)
        name = name["name"]
        
        active_order_query = f"SELECT order_id, date, payment_method, total_price, order_status, patient_id, pharmacy_id, name, phone_number FROM drug_order INNER JOIN user ON drug_order.pharmacy_id = user.UID WHERE order_status = 1 AND patient_id = {self.uid}"

        past_order_query = f"SELECT order_id, date, payment_method, total_price, order_status, patient_id, pharmacy_id, name, phone_number FROM drug_order INNER JOIN user ON drug_order.pharmacy_id = user.UID WHERE order_status = 0 AND patient_id = {self.uid}"

        active_orders = self.patient_service.fetch_all(query=active_order_query)
        past_orders = self.patient_service.fetch_all(query=past_order_query)
        
        active_drug_list = []
        for i,ord in enumerate(active_orders):
            active_drug_list.append("") 
            drug_query = f"SELECT drug_name FROM order_contains_drug NATURAL JOIN Drug WHERE order_id = {ord['order_id']}"
            drugs = self.patient_service.fetch_all(query=drug_query)
            for drug in drugs:
                print(drug)
                active_drug_list[i] += drug["drug_name"] + ", "
        for i in range(len(active_drug_list)):
            active_drug_list[i] = active_drug_list[i][:-2]
        print(active_drug_list)
        past_drug_list = []
        for i,ord in enumerate(past_orders):
            past_drug_list.append("") 
            drug_query = f"SELECT drug_name FROM order_contains_drug NATURAL JOIN Drug WHERE order_id = {ord['order_id']}"
            drugs = self.patient_service.fetch_all(query=drug_query)
            for drug in drugs:
                past_drug_list[i] += drug["drug_name"] + ", "
        for i in range(len(past_drug_list)):
            past_drug_list[i] = past_drug_list[i][:-2]
        return render_template("patient/patient_orders.html", name=name, balance=balance, active_orders=active_orders, active_drug_list=active_drug_list, past_orders=past_orders, past_drug_list=past_drug_list, notifications=self.patient_service.fetch_notifications(self.uid))

    def post(self):
        if "Home" in request.form:
            return redirect(url_for('patient'))
        elif "ordermedicine" in request.form:
            return redirect(url_for("ordermedicine"))
        elif "oldprescriptions" in request.form:
            return redirect(url_for("old_prescriptions"))
        #elif "logout" in request.form:
            #pass
        elif "addbalance" in request.form:
            return redirect(url_for("patient_balance"))
        elif "editprofile" in request.form:
            return redirect(url_for("patient_edit"))
        elif "assistant" in request.form:
            return redirect(url_for('assistant'))
        elif "vieworders" in request.form:
            return redirect(url_for('patient_orders'))


        
