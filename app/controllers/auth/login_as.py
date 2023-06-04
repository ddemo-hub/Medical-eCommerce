from src.services.base_service import BaseService

from flask.views import MethodView
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session

class LoginAs(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True
    userrole = None

    def __init__(self, database_service, auth_service):
        super().__init__()
        self.database_service = database_service
        self.auth_service = auth_service
    
    @BaseService.login_required
    def get(self):
        uid = session['uid']
        self.userrole = self.auth_service.fetch_all(f'SELECT * FROM user_roles WHERE UID = {int(uid)}')
        print(self.userrole)

        message = ''
        log = ''
        return render_template('auth/login_as.html', message = message, log=log, userrole=self.userrole)
    
    def post(self):
        message = ''
        log = ''
        uid = session['uid']
        self.userrole = self.auth_service.fetch_all(f'SELECT * FROM user_roles WHERE UID = {int(uid)}')
        if 'login_Doctor' in request.form:
            session['Role'] = 'Doctor'
            return redirect(url_for('doctor_main'))
        elif 'login_Patient' in request.form:
            session['Role'] = 'Patient'
            return redirect(url_for('patient'))
        elif 'login_Pharmacy' in request.form:
            session['Role'] = 'Pharmacy'
            return redirect(url_for('pharmacy_main'))
        
        return render_template('auth/login_as.html', message = message, log=log, userrole=self.userrole)