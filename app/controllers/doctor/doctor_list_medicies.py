from datetime import datetime
from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class DoctorListMedicines(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, doctor_service):
        super().__init__()
        self.database_service = database_service
        self.doctor_service = doctor_service

        self.doctor_info = None
        self.medicines = []
    
    def initget(self):
        """session["UID"] = 1"""
        uid = session["UID"]
        print(uid)
        self.doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN Role WHERE UID = {uid} AND role = "Doctor"')
        self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug')
        
    def get(self):
        message = ''
        print(self.doctor_info)
        self.initget()
        return render_template('doctor/list_medicines.html', message = message,doctor_info = self.doctor_info, medicines=self.medicines)
    
    def post(self):
        message=''
        """session["UID"] = 1"""
        uid = session["UID"]
        self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug')
        self.doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN Role WHERE UID = {uid} AND role = "Doctor"')

        # Medicine search bar(s)
        if "search_name" in request.form:
            name = request.form["search_name"]
            self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE drug_name LIKE "%{name}%"')
        elif "search_company" in request.form:
            name = request.form["search_company"]
            self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE company LIKE "%{name}%"')
        elif "search_restricted" in request.form:
            name = request.form["search_restricted"]
            self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE is_restricted = {name}')
        elif "search_year" in request.form:
            year = request.form["search_year"]
            if len(year) > 0:
                self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE production_year = {year}')
        elif "search_class" in request.form:
            name = request.form["search_class"]
            self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE drug_class LIKE "%{name}%"')
        elif "search_info" in request.form:
            name = request.form["search_info"]
            self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE drug_info LIKE "%{name}%"')
        elif "search_use_count" in request.form:
            name = request.form["search_use_count"]
            if len(name) > 0:
                self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE use_count = {name}')
        
        if "Home" in request.form:
            return redirect(url_for('doctor_main'))
        if "add_prescription" in request.form:
            return redirect(url_for('add_prescription'))
        if "past_prescriptions" in request.form:
            return redirect(url_for('doctor_past_prescriptions'))
        if "list_medicines" in request.form:
            return redirect(url_for('doctor_list_medicines'))
            
        return render_template('doctor/list_medicines.html', message = message,doctor_info = self.doctor_info, medicines=self.medicines)