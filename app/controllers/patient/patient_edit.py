from src.services.base_service import BaseService
from flask.views import MethodView
from flask import render_template, redirect, request, url_for

class PatientEdit(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, patient_service):
        super().__init__()
        self.database_service = database_service
        self.patient_service = patient_service
    
    @BaseService.login_required
    def get(self):
        balance_query = f"SELECT Wallet_balance FROM Patient " +\
                               f"WHERE UID = {self.uid}"
        patient_query = f"SELECT * FROM User NATURAL JOIN Patient WHERE UID = {self.uid}"

        name_query = f"SELECT name FROM User " +\
                               f"WHERE UID = {self.uid}"
        name = self.patient_service.fetch_one(query=name_query)
        name = name["name"]
        
        balance = self.patient_service.fetch_one(query=balance_query)
        patient = self.patient_service.fetch_one(query=patient_query)
        return render_template("patient/patient_edit.html", name=name, balance=balance, patient=patient, notifications=self.patient_service.fetch_notifications(self.uid))

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
        elif "notification" in request.form:
            if request.form.get("notification") == "Allow":
                notification_query = f"UPDATE Patient SET Allow_notifications=TRUE WHERE UID={self.uid}"
            else:
                notification_query = f"UPDATE Patient SET Allow_notifications=FALSE WHERE UID={self.uid}"
            self.database_service.dml(notification_query)
            return redirect(url_for('patient_edit'))
        elif "updateprofile" in request.form:
            name = request.form.get("name")
            phone = request.form.get("phone")
            birthday = request.form.get("date")
            address = request.form.get("address")
            if name != '':
                name = "\"" + name + "\""
                name_query = f'UPDATE User SET name={name} WHERE UID={self.uid}'
                self.patient_service.dml(name_query)
                self.name = name
            if phone != '':
                phone_query = f"UPDATE User SET Phone_number={phone} WHERE UID={self.uid}"
                self.patient_service.dml(phone_query)
            if birthday != '':
                birthday = "\"" + birthday + "\""
                bd_query = f"UPDATE Patient SET birthday={birthday} WHERE UID={self.uid}"
                self.patient_service.dml(bd_query)
            if address != '':
                address = "\"" + address + "\""
                address_query = f"UPDATE Patient SET Address={address} WHERE UID={self.uid}"
                self.patient_service.dml(address_query)
            return redirect(url_for('patient_edit'))
        elif "assistant" in request.form:
            return redirect(url_for('assistant'))
        elif "vieworders" in request.form:
            return redirect(url_for('patient_orders'))

        
