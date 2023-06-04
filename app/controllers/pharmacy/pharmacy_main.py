from src.services.base_service import BaseService
from src.services.database_service import DatabaseService

from flask.views import MethodView
from flask import render_template, request, redirect, url_for, session

class PharmacyMain(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service: DatabaseService):
        super().__init__()
        self.database_service = database_service

    @BaseService.login_required
    def get(self):
        all_items_query = f"SELECT Inventory.serial_number, Inventory.expiration_date, Drug.drug_name " + \
                          f"FROM Inventory JOIN Drug ON Inventory.drug_id = Drug.drug_id " + \
                          f"WHERE Inventory.pharmacy_id = {self.uid} " + \
                          f"ORDER BY Drug.drug_name ASC;"
        
        df_all_items = self.database_service.dql(query=all_items_query, columns=["serial_number", "expiration_date", "drug_name"])
        inventory = df_all_items.to_dict("records")

        return render_template("pharmacy/pharmacy_main.html", name=self.name, inventory=inventory)

    @BaseService.login_required
    def post(self):
        if "Home" in request.form:
            return redirect(url_for("pharmacy_main"))
        elif "logout" in request.form:
            session.clear()
            session["uid"] = None
            session["logged_in"] = False
            return redirect(url_for('login'))     
        elif "add_drug" in request.form:
            return redirect(url_for("pharmacy_add_drug"))
        elif "view_orders":
            return redirect(url_for("pharmacy_orders"))