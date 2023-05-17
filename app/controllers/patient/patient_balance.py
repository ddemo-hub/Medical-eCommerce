from src.services.base_service import BaseService
from flask.views import MethodView
from flask import render_template, redirect, request, url_for

class PatientBalance(MethodView, BaseService):
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

        return render_template("patient/patient_balance.html", name=name, balance=balance, notifications=self.patient_service.fetch_notifications(self.uid))

    def post(self):
        if "Home" in request.form:
            return redirect(url_for('patient'))
        #elif "ordermedicine" in request.form:
            #pass
        elif "oldprescriptions" in request.form:
            return redirect(url_for("old_prescriptions"))
        #elif "logout" in request.form:
            #pass
        elif "addbalance" in request.form:
            return redirect(url_for("patient_balance"))
        elif "editprofile" in request.form:
            return redirect(url_for("patient_edit"))
        elif "updatebalance" in request.form:
            balance_query = f"SELECT Wallet_balance FROM Patient " +\
                               f"WHERE UID = {self.uid}"
            balance = self.patient_service.fetch_one(query=balance_query)
            newbalance = balance["Wallet_balance"] + int(request.form.get("balance"))
            balance_update_query = f"UPDATE Patient SET Wallet_balance = {newbalance} WHERE UID = {self.uid}"
            self.database_service.dml(balance_update_query)
            return redirect(url_for("patient_balance"))
        elif "assistant" in request.form:
            return redirect(url_for('assistant'))

        
