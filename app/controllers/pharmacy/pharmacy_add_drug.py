from src.services.base_service import BaseService
from src.services.database_service import DatabaseService

from flask.views import MethodView
from flask import render_template, request, redirect, url_for, session

class PharmacyAddDrug(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service: DatabaseService):
        super().__init__()
        self.database_service = database_service

    @BaseService.login_required
    def get(self):
        df_drugs = self.database_service.dql("SELECT drug_id, drug_name FROM Drug;", columns=["drug_id", "drug_name"])
        all_drugs = df_drugs.to_dict("records")

        return render_template("pharmacy/pharmacy_add_drug.html", name=self.name, message="", drugs=all_drugs)
    
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
            df_drugs = self.database_service.dql("SELECT drug_id, drug_name FROM Drug;", columns=["drug_id", "drug_name"])
            all_drugs = df_drugs.to_dict("records")

            message = "Something went wrong!"
            if request.form.keys() >= {"drug_id", "expiration_date"}:
                insert_drug_query = f"INSERT INTO Inventory(pharmacy_id, drug_id, expiration_date) " + \
                                    f"VALUES({self.uid}, {request.form['drug_id']}, '{request.form['expiration_date']}');"

                self.database_service.dml(insert_drug_query)
                message = "Successfully added new drug"
            
            return render_template("pharmacy/pharmacy_add_drug.html", name=self.name, message=message, drugs=all_drugs)