from src.services.base_service import BaseService
from flask.views import MethodView
from flask import render_template, redirect, request, url_for

class Assistant(MethodView, BaseService):
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
        medicine_query = f"SELECT D.drug_name as name, D.Drug_ID as id FROM Assistant_track_Drug ATD NATURAL JOIN Drug D WHERE ATD.Assistant_ID = {self.uid} AND DATE_ADD(ATD.Last_time_taken, INTERVAL(ATD.Frequency) DAY) = CURDATE() AND ATD.Pill_count <> 0 AND ATD.Expiration_date >= CURDATE()"
        reminder_query = f"SELECT D.drug_name as name FROM Assistant_track_Drug ATD NATURAL JOIN Drug D WHERE ATD.Assistant_ID = {self.uid} AND ATD.Pill_count / ATD.Frequency <= 3 AND ATD.Expiration_date >= CURDATE()"
        exp_query = f"SELECT D.drug_name as name FROM Assistant_track_Drug ATD NATURAL JOIN Drug D WHERE ATD.Assistant_ID = {self.uid} AND DATE_ADD(CURDATE(), INTERVAL(5) DAY) >= ATD.Expiration_date"
        name_query = f"SELECT name FROM User " +\
                               f"WHERE UID = {self.uid}"
        name = self.patient_service.fetch_one(query=name_query)
        name = name["name"]

        medicine = self.patient_service.fetch_all(query=medicine_query)
        reminder = self.patient_service.fetch_all(query=reminder_query)
        balance = self.patient_service.fetch_one(query=balance_query)
        patient = self.patient_service.fetch_one(query=patient_query)
        expiration = self.patient_service.fetch_all(query=exp_query)

        reminder_str = ""
        for rem in reminder:
            reminder_str += rem["name"] + ", "
        
        if reminder_str != "":
            reminder_str = reminder_str[:-2]

        exp_str = ""
        for exp in expiration:
            exp_str += exp["name"] + ", "
        
        if exp_str != "":
            exp_str = exp_str[:-2]
        print(medicine)
        return render_template("patient/assistant.html", name=name, balance=balance, patient=patient, reminder=reminder_str, medicine = medicine, expiration=exp_str)

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
        elif "assistant" in request.form:
            return redirect(url_for('assistant'))
        elif "mark" in request.form:
            drug_id = request.form.get("mark")
            mark_query = f"UPDATE Assistant_track_Drug SET Last_time_taken=CURDATE(), Pill_count=Pill_count-1 WHERE Assistant_ID={self.uid} AND Drug_ID={drug_id}"
            self.database_service.dml(mark_query)
            return redirect(url_for('assistant'))
        elif "vieworders" in request.form:
            return redirect(url_for('patient_orders'))
        

        
