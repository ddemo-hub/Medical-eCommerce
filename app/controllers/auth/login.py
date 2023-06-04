from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session

class Login(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, auth_service):
        super().__init__()
        self.database_service = database_service
        self.auth_service = auth_service
    
    def get(self):
        message = ''
        log = ''
        # TODO add other session variables
        session['loggedin'] = False
        session['uid'] = None
        session['name'] = None
        session['role'] = None
        
        return render_template('auth/login.html', message = message, log=log)
    
    def post(self):
        message = ''
        log = ''
        if 'uid' in request.form and 'password' in request.form:
            uid = request.form['uid']
            password = request.form['password']

            if (len(uid) == 0 or len(password) == 0):
                message = 'Please fill all necessary fields'
                return render_template('auth/login.html', message = message, log=log)

            self.userrole = self.auth_service.fetch_all(f'SELECT uid,name,role FROM User NATURAL JOIN user_roles WHERE UID = {int(uid)} AND password = "{password}"')
            print(self.userrole)

            if len(self.userrole) > 0:              
                session['logged_in'] = True
                session['uid'] = int(self.userrole[0]['uid'])
                session['name'] = self.userrole[0]['name']
                return redirect(url_for('login_as'))
            else:
                message = 'User ID or password is wrong'
        return render_template('auth/login.html', message = message, log=log)