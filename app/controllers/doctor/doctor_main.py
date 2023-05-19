from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class DoctorMain(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, doctor_service):
        super().__init__()
        self.database_service = database_service
        self.doctor_service = doctor_service
    
    def get(self):
        message = ''
        # 'SELECT * FROM User NATURAL JOIN Role WHERE UID = % s AND role = %s', (uid, 'Doctor')
        uid = session["UID"]
        doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN Role WHERE UID = {uid} AND role = "Doctor"')
        last_prescriptions = self.doctor_service.fetch_all(f'SELECT * FROM Prescription NATURAL JOIN Doctor_Prescribes_Prescription WHERE doctor_id = {uid}')

        return render_template('doctor/doctor_main.html', message = message,doctor_info = doctor_info)
    
    def post(self):
        if "add_prescription" in request.form:
            return redirect(url_for('add_prescription'))