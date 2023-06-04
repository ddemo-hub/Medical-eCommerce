from datetime import datetime
from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class DoctorViewPrescriptionDetails(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, doctor_service):
        super().__init__()
        self.database_service = database_service
        self.doctor_service = doctor_service

        self.doctor_info = None
        self.prescription = None
        self.prescribed_medicines = None
    
    @BaseService.login_required
    def get(self):
        message = ''
        uid = session["uid"]
        self.doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN user_roles WHERE UID = {uid} AND role = "Doctor"')
        self.prescription = self.doctor_service.fetch_one(f'SELECT prescription_id,doctor_id,patient_id,DATE_FORMAT(create_date,"%d %m %Y") as create_date,DATE_FORMAT(expiration_date,"%d %m %Y") as expiration_date, doctors_notes FROM Prescription NATURAL JOIN Doctor_Prescribes_Prescription WHERE prescription_id = {session["prescription_id"]}')
        self.prescribed_medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug NATURAL JOIN drug_in_prescription WHERE prescription_id = {session["prescription_id"]}')
        return render_template('doctor/prescription_details.html', message = message,doctor_info = self.doctor_info, prescription=self.prescription, prescribed_medicines=self.prescribed_medicines)
    
    def post(self):
        message=''

        if "Home" in request.form:
            return redirect(url_for('doctor_main'))
        if "add_prescription" in request.form:
            return redirect(url_for('add_prescription'))
        if "past_prescriptions" in request.form:
            return redirect(url_for('doctor_past_prescriptions'))
        if "list_medicines" in request.form:
            return redirect(url_for('doctor_list_medicines'))
        if "logout" in request.form:
            session.clear()
            session["uid"] = None
            session["logged_in"] = False
            return redirect(url_for('login'))
        