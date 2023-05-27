from datetime import datetime
from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class AddMedicineToPrescription(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, doctor_service):
        super().__init__()
        self.database_service = database_service
        self.doctor_service = doctor_service

        self.doctor_info = None
        self.medicines = []
        self.prescribed_medicines = []
        self.doctors_notes = ""
    
    def initget(self,meaasge=""):
        uid = session["UID"]
        print(uid)
        self.doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN Role WHERE UID = {uid} AND role = "Doctor"')
        self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug')
        self.prescribed_medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug NATURAL JOIN drug_in_prescription WHERE prescription_id = {session["prescription_id"]}')
        self.doctors_notes = self.doctor_service.fetch_one(f'SELECT doctors_notes FROM prescription WHERE prescription_id = {session["prescription_id"]}')
        print(self.prescribed_medicines)
    def get(self):
        message = ''
        self.initget()
        return render_template('doctor/add_medicine_to_prescription.html', message = message,doctor_info = self.doctor_info, medicines=self.medicines,prescribed_medicines=self.prescribed_medicines, doctors_notes=self.doctors_notes)
    
    def post(self):
        message=''
        uid = session["UID"]
        self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug')
        self.prescribed_medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug NATURAL JOIN drug_in_prescription WHERE prescription_id = {session["prescription_id"]}')
        self.doctors_notes = self.doctor_service.fetch_one(f'SELECT doctors_notes FROM prescription WHERE prescription_id = {session["prescription_id"]}')
        self.doctor_info = self.doctor_service.fetch_one(f'SELECT * FROM User NATURAL JOIN Role WHERE UID = {uid} AND role = "Doctor"')
        # Medicine search bar(s)
        if "search_name" in request.form:
            name = request.form["search_name"]
            print("\n\n\n", name)
            self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE drug_name LIKE "%{name}%"')
        
        elif "search_company" in request.form:
            name = request.form["search_company"]
            print("\n\n\n", name)
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
            print("\n\n\n", name)
            self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE drug_class LIKE "%{name}%"')
        
        elif "search_info" in request.form:
            name = request.form["search_info"]
            print("\n\n\n", name)
            self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE drug_info LIKE "%{name}%"')
        
        elif "search_use_count" in request.form:
            name = request.form["search_use_count"]
            if len(name) > 0:
                self.medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug WHERE use_count = {name}')
        
        if "add_medicine" in request.form:
            drug_id = request.form["add_medicine"]
            print("drug:", drug_id)
            try:
                ex = self.doctor_service.dml(f'INSERT INTO drug_in_prescription (drug_id, prescription_id, count) VALUES ({drug_id},{session["prescription_id"]},"1")')
                print(ex, type(ex))
                self.prescribed_medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug NATURAL JOIN drug_in_prescription WHERE prescription_id = {session["prescription_id"]}')
                message = "added medicine to presription"
            except Exception as ex:
                print("EXC")
                message = "medicine already exists in presription"
        
        if "remove_medicine" in request.form:
            drug_id = request.form["remove_medicine"]
            print("drug:", drug_id)
            try:
                self.doctor_service.dml(f'DELETE FROM drug_in_prescription WHERE drug_id = {drug_id} AND prescription_id = {session["prescription_id"]}')
                self.prescribed_medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug NATURAL JOIN drug_in_prescription WHERE prescription_id = {session["prescription_id"]}')
                message = "removed medicine from prescription"
            except Exception as ex:
                message = "an error occured during removal"
        
        if "update_medicine" in request.form:
            drug_id = request.form["update_medicine"]
            count = request.form["update_medicine_count"]

            try:
                self.doctor_service.dml(f'UPDATE drug_in_prescription SET count = {count} WHERE drug_id = {drug_id} AND prescription_id = {session["prescription_id"]}')
                self.prescribed_medicines = self.doctor_service.fetch_all(f'SELECT * FROM Drug NATURAL JOIN drug_in_prescription WHERE prescription_id = {session["prescription_id"]}')
                message = "updated medicine count"
            except Exception as ex:
                message = "drug count must be positive"
        
        if "update_notes" in request.form:
            doctors_notes = request.form["doctors_notes"]
            print(doctors_notes)
            if len(doctors_notes) < 10:
                message = "doctor's notes is too short, at least 10 characters are required"
            else:
                try:
                    self.doctor_service.dml(f'UPDATE prescription SET doctors_notes = "{doctors_notes}" WHERE prescription_id = {session["prescription_id"]}')
                    self.doctors_notes = self.doctor_service.fetch_one(f'SELECT doctors_notes FROM prescription WHERE prescription_id = {session["prescription_id"]}')
                    message = "updated doctor's notes"
                except Exception as ex:
                    message = "error occured during updating doctor's notes"
            
        if "finalize_prescription" in request.form:
            return redirect(url_for('doctor_main'))

            
        return render_template('doctor/add_medicine_to_prescription.html', message = message,doctor_info = self.doctor_info, medicines=self.medicines,prescribed_medicines=self.prescribed_medicines, doctors_notes=self.doctors_notes)