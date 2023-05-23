from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class DoctorPastPrescriptions(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, doctor_service):
        session["UID"] = 1
        super().__init__()
        self.database_service = database_service
        self.doctor_service = doctor_service
        self.doctor_info = ""
        self.last_prescriptions = []
    
    def get(self):
        message = ''
        print("\n\nHERE\n\n")
        uid = session["UID"]
        doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN Role WHERE UID = {uid} AND role = "Doctor"')
        self.last_prescriptions = self.doctor_service.fetch_all(f'SELECT doctor_id,patient_id,DATE_FORMAT(create_date,"%d %m %Y") as create_date,DATE_FORMAT(expiration_date,"%d %m %Y") as expiration_date FROM Prescription NATURAL JOIN Doctor_Prescribes_Prescription WHERE doctor_id = {uid} ORDER BY create_date DESC;')
        print("\n\n", self.last_prescriptions)
        return render_template('doctor/past_prescriptions.html', message = message,doctor_info = doctor_info, last_prescriptions=self.last_prescriptions)
    
    def post(self):
        if "add_prescription" in request.form:
            return redirect(url_for('add_prescription'))