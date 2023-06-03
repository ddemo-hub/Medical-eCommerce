from src.services.base_service import BaseService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from datetime import datetime

class RegisterPatient(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, auth_service):
        super().__init__()
        self.database_service = database_service
        self.auth_service = auth_service
    
    def get(self):
        message = ''
        log = ''
        max_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        # print(max_date)
        return render_template('auth/register_patient.html', message = message, log = log, max_date=max_date)
    
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
            
            account = self.database_service.dql(f'SELECT UID FROM User WHERE UID = {uid}', ["UID"])
            # if user does not exist, add account
            if account.empty:
                self.database_service.dml(f'INSERT INTO User (UID, Name, Password, Phone_number) VALUES ({uid},"{name}","{password}",{phone})')
                log += "ADDED USER"
            # else, check other credentials name and phone number
            else:
                # if other credentials is wrong, exit
                account = self.auth_service.fetch_one(f'SELECT UID FROM User WHERE UID = {uid} AND password = "{password}" AND Phone_Number = {phone}')
                if account == None:
                    message = "Credendials for this user is wrong"
                    return render_template('auth/register_patient.html', message = message, log = log)
            
            # if user has Patient role, return
            account = self.database_service.dql(f'SELECT role FROM Role WHERE UID = {uid}', ["role"])
            account = account.to_dict('list')["role"]
            for acc in account:
                if acc == 'Patient' or len(account) == 2:
                    message = "Role already exists"
                    return render_template('auth/register_patient.html', message = message, log = log)
            
            # if birthday date is not in past return
            print(datetime.strptime(birthday, "%Y-%m-%d"))
            if datetime.strptime(birthday, "%Y-%m-%d") > datetime.now():
                message = "Birthdate must be before today"
                return render_template('auth/register_patient.html', message = message, log = log)

            account = self.database_service.dql(f'SELECT Name FROM User WHERE UID = \'{uid}\' AND Password = \'{password}\'', ["Name"])
            log += "CHOSEN ACCOUNT" + str(account)
            # if password is correct, insert new role
            if not account.empty:
                try: 
                    self.auth_service.dml(f'INSERT INTO Patient (UID,Address,Birthday) VALUES ({uid},"{address}","{birthday}")')
                    message = "New patient added to the system"
                except Exception as e:
                    message = "Unknown error, check all credentials"
                    return render_template('auth/register_patient.html', message = message, log = log)
            else:
                message = "password is wrong"
                return render_template('auth/register_patient.html', message = message, log = log)
            
            
            
        elif request.method == 'POST':
            message = 'Please fill all the fields!'
        
        return render_template('auth/register_patient.html', message = message, log = log)