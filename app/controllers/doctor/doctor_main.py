from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class DoctorMain(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service):
        super().__init__()
        self.database_service = database_service
    
    def get(self):
        message = ''
        # 'SELECT * FROM User NATURAL JOIN Role WHERE UID = % s AND role = %s', (uid, 'Doctor')
        data = self.database_service.dql(f'SELECT UID,Name,role FROM User NATURAL JOIN Role WHERE UID = {session["UID"]} AND role = "Doctor"', ["UID","Name","role"])

        return render_template('doctor/doctor_main.html', message = message,data = data)