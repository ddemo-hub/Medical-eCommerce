from src.services.base_service import BaseService
from flask.views import MethodView
from flask import render_template, request, redirect, url_for

class PatientMain(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, patient_service):
        super().__init__()
        self.database_service = database_service
        self.patient_service = patient_service
    
    @BaseService.login_required
    def get(self):
        balance_query = f"SELECT Wallet_balance FROM Patient " +\
                               f"WHERE UID = {self.uid}"
        
        current_medicine_query = f"SELECT D.drug_name as name, D.drug_info as info, DATE_ADD(CURDATE(), INTERVAL (ATD.Pill_count / ATD.Frequency) DAY) as date FROM Assistant_track_Drug ATD NATURAL JOIN Drug D WHERE ATD.Assistant_ID = {self.uid}"
    
        active_prescriptions_query = f"SELECT * FROM Prescription NATURAL JOIN Doctor_prescribes_Prescription INNER JOIN User ON Doctor_prescribes_Prescription.Doctor_ID = User.UID " +\
                                        f"WHERE Patient_ID = {self.uid} AND is_valid = TRUE AND Expiration_Date >= CURDATE() ORDER BY Expiration_date"
    
        name_query = f"SELECT name FROM User " +\
                               f"WHERE UID = {self.uid}"
        name = self.patient_service.fetch_one(query=name_query)
        name = name["name"]
        
        balance = self.patient_service.fetch_one(query=balance_query)
        
        current_medicine = self.patient_service.fetch_all(query=current_medicine_query)
        active_prescriptions = self.patient_service.fetch_all(query=active_prescriptions_query)
        
        drug_list = []
        for i,presc in enumerate(active_prescriptions):
            print(presc)
            drug_list.append("") 
            drug_query = f"SELECT drug_name, Prescription_ID FROM Prescription NATURAL JOIN Drug_in_Prescription NATURAL JOIN Drug WHERE Prescription_ID = {presc['prescription_id']}"
            drugs = self.patient_service.fetch_all(query=drug_query)
            for drug in drugs:
                drug_list[i] += drug["drug_name"] + ", "
        for i in range(len(drug_list)):
            drug_list[i] = drug_list[i][:-2]
        return render_template("patient/patient_main.html", name=name, balance=balance, current_medicine=current_medicine, active_prescriptions=active_prescriptions, drug_list=drug_list, notifications=self.patient_service.fetch_notifications(self.uid))

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
        elif "vieworders" in request.form:
            return redirect(url_for('patient_orders'))

        
