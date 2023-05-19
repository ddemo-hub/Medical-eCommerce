from datetime import datetime
from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class AddPrescription(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, doctor_service):
        super().__init__()
        self.database_service = database_service
        self.doctor_service = doctor_service

        self.doctor_info = None
        self.min_date = None
        self.patients = None
    
    def  initget(self,meaasge=""):
        uid = session["UID"]
        print(uid)
        self.doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN Role WHERE UID = {uid} AND role = "Doctor"')
        self.min_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        self.patients = self.doctor_service.fetch_all(f'SELECT UID FROM Role WHERE role = "Patient" AND UID <> {uid}')

    def get(self):
        message = ''
        self.initget()
        return render_template('doctor/add_prescription.html', message = message,doctor_info = self.doctor_info, min_date=self.min_date,patients=self.patients)
    
    def post(self):
        uid = session["UID"]
        if "prescription_continue" in request.form:
            if not "expiration_date" in request.form or not "patient_id" in request.form:
                message = "fill all the fields"
                return redirect(url_for('add_prescription'))
            else:
                expiration_date = request.form["expiration_date"]
                print(expiration_date,request.form["patient_id"])
                patient_id = request.form["patient_id"]
                try:
                    self.doctor_service.dml(f'INSERT INTO Prescription (create_date,expiration_date,is_valid,patient_id) VALUES (CURDATE(),"{expiration_date}",1,{patient_id})')
                    prescription_id = self.doctor_service.fetch_one(f'SELECT prescription_id FROM Prescription WHERE patient_id = {patient_id} ORDER BY prescription_id DESC LIMIT 1')
                    print(prescription_id["prescription_id"])
                    prescription_id=prescription_id["prescription_id"]
                    self.doctor_service.dml(f'INSERT INTO doctor_prescribes_prescription (doctor_id, prescription_id) VALUES ({uid},{prescription_id})')
                    
                    session["prescription_id"] = prescription_id
                    return redirect(url_for('add_medicine_to_prescription'))
                except Exception as ex:
                    message = "error occured while in query"
                    print(message)
                    return redirect(url_for('add_prescription'))

            

        return redirect(url_for('add_prescription'))