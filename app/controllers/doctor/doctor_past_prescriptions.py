from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class DoctorPastPrescriptions(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, doctor_service):
        """session["UID"] = 1"""
        super().__init__()
        self.database_service = database_service
        self.doctor_service = doctor_service
        self.doctor_info = ""
        self.last_prescriptions = []
    
    def get(self):
        message = ''
        uid = session["UID"]
        doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN Role WHERE UID = {uid} AND role = "Doctor"')
        self.last_prescriptions = self.doctor_service.fetch_all(f'SELECT prescription_id,doctor_id,patient_id,DATE_FORMAT(create_date,"%d %m %Y") as create_date,DATE_FORMAT(expiration_date,"%d %m %Y") as expiration_date, is_valid FROM Prescription NATURAL JOIN Doctor_Prescribes_Prescription WHERE doctor_id = {uid} ORDER BY create_date DESC;')
        return render_template('doctor/past_prescriptions.html', message = message,doctor_info = doctor_info, last_prescriptions=self.last_prescriptions)
    
    def post(self):
        message=''

        if "prescription_details" in request.form:
            session["prescription_id"] = request.form["prescription_details"]
            print("PRESC ID:", session["prescription_id"])
            return redirect(url_for('doctor_view_prescription_details'))

        if "Home" in request.form:
            return redirect(url_for('doctor_main'))
        if "add_prescription" in request.form:
            return redirect(url_for('add_prescription'))
        if "past_prescriptions" in request.form:
            return redirect(url_for('doctor_past_prescriptions'))
        if "list_medicines" in request.form:
            return redirect(url_for('doctor_list_medicines'))
        
        return render_template('doctor/past_prescriptions.html', message = message,doctor_info = self.doctor_info, last_prescriptions=self.last_prescriptions)
