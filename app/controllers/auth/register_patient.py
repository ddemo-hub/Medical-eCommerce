from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from datetime import datetime

class RegisterPatient(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service):
        super().__init__()
        self.database_service = database_service
    
    def get(self):
        message = ''
        log = ''
        return render_template('auth/register_patient.html', message = message, log = log)
    
    def post(self):
        message = ''
        log = ''
        if 'uid' in request.form and 'name' in request.form and 'password' in request.form and 'phone' in request.form and 'address' in request.form and 'birthday' in request.form:
            uid = request.form['uid']
            name = request.form['name']
            password = request.form['password']
            phone = request.form['phone']
            address = request.form['address']
            birthday = request.form['birthday']

            # if birthday date is not in past return
            print("\n\n\n",birthday)
            birthday = datetime.strptime(birthday, "%Y-%m-%d").strftime("%Y-%m-%d")
            if datetime.strptime(birthday, "%Y-%m-%d") > datetime.now():
                message = "Birthdate must be before today"
                return render_template('auth/register_patient.html', message = message, log = log)
            
            
            if int(phone) < 5000000000:
                return render_template('auth/register_patient.html', message ="phone number is invalid", log = log)

            account = self.database_service.dql(f'SELECT UID FROM User WHERE UID = {uid}', ["UID"])
            log += "USERS WITH UID" + str(account)
            # if user does not exist, add account
            if account.empty:
                self.database_service.dml(f'INSERT INTO User (UID, Name, Password, Phone_number) VALUES ({uid},"{name}","{password}",{phone})')
                log += "ADDED USER"
            
            # if user has Patient role, return
            account = self.database_service.dql(f'SELECT role FROM Role WHERE UID = {uid}', ["role"])
            account = account.to_dict('list')["role"]
            for acc in account:
                if acc == 'Patient' or len(account) == 2:
                    message = "Role already exists"
                    return render_template('auth/register_patient.html', message = message, log = log)
            
            account = self.database_service.dql(f'SELECT Name FROM User WHERE UID = \'{uid}\' AND Password = \'{password}\'', ["Name"])
            log += "CHOSEN ACCOUNT" + str(account)
            # if password is correct, insert new role
            if not account.empty:
                if self.database_service.dml(f'INSERT INTO Patient (UID,Address,Birthday) VALUES ({uid},"{address}","{birthday}")'):
                    message = "New patient added to the system"
                else:
                    message = "Unknown error, check all credentials"
                    return render_template('auth/register_patient.html', message = message, log = log)
            else:
                message = "password is wrong"
                return render_template('auth/register_patient.html', message = message, log = log)
            
            
            
        elif request.method == 'POST':
            message = 'Please fill all the fields!'
        
        return render_template('auth/register_patient.html', message = message, log = log)