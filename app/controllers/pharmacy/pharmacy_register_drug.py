from src.services.base_service import BaseService
from src.services.database_service import DatabaseService

from flask.views import MethodView
from flask import render_template, request, redirect, url_for, session

class PharmacyRegisterDrug(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service: DatabaseService):
        super().__init__()
        self.database_service = database_service

    @BaseService.login_required
    def get(self):
        return render_template("pharmacy/pharmacy_register_drug.html", name=self.name, message="")
    
    @BaseService.login_required
    def post(self):
        if "Home" in request.form:
            return redirect(url_for("pharmacy_main"))
        elif "logout" in request.form:
            session.clear()
            session["uid"] = None
            session["logged_in"] = False
            return redirect(url_for('login'))           
        else:
            message = "Something went wrong!"
            if request.form.keys() >= {"drug_name", "company", "is_restricted", "price", "production_year", "drug_class", "drug_info", "use_count", "age_group", "side_effects"}:
                values = request.form
                register_drug_query = f"INSERT INTO Drug(drug_name, company, is_restricted, price, production_year, drug_class, drug_info, use_count, age_group, side_effects) " + \
                                      f"VALUES('{values['drug_name']}', '{values['company']}', {int(values['is_restricted'])}, {int(values['price'])}, {int(values['production_year'])}, " + \
                                      f"'{values['drug_class']}', '{values['drug_info']}', {int(values['use_count'])}, '{values['age_group']}', '{values['side_effects']}');"

                self.database_service.dml(register_drug_query)
                message = "Successfully added new drug"
            
            return render_template("pharmacy/pharmacy_register_drug.html", name=self.name, message=message)