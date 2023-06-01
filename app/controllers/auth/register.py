from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class Register(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service):
        super().__init__()
        self.database_service = database_service
    
    def get(self):
        message = ''
        log = ''
        
        return render_template('auth/register.html', message = message)
    
    def post(self):
        message = ''
        if request.method == 'POST' and 'doctor_register' in request.form:
            print("\n\ndr\n\n")
            return redirect(url_for('register_doctor'))
        elif request.method == 'POST' and 'patient_register' in request.form:
            return redirect(url_for('register_patient'))
        elif request.method == 'POST' and 'pharmacy_register' in request.form:
            return redirect(url_for('register_pharmacy'))
        
        return render_template('auth/register.html', message = message)