from src.services.base_service import BaseService

from flask.views import MethodView
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session

class LoginAs(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True
    userrole = None

    def __init__(self, database_service):
        super().__init__()
        self.database_service = database_service
    
    @BaseService.login_required
    def get(self):
        uid = session['uid']
        self.userrole = self.database_service.dql(f'SELECT UID,role FROM User NATURAL JOIN Role WHERE UID = {uid}', ["UID","role"])
        self.userrole = self.userrole.to_dict('list')["role"]

        message = ''
        log = ''
        return render_template('auth/login_as.html', message = message, log=log, userrole=self.userrole)
    
    def post(self):
        message = ''
        log = ''
        if 'login_Doctor' in request.form:
            session['Role'] = 'Doctor'
            return redirect(url_for('doctor_main'))
        elif 'login_Patient' in request.form:
            session['Role'] = 'Patient'
            return redirect(url_for('patient'))
        elif 'login_Pharmacy' in request.form:
            session['Role'] = 'Pharmacy'
            return redirect(url_for('pharmacy_orders'))
        
        return render_template('auth/login_as.html', message = message, log=log, userrole=self.userrole)