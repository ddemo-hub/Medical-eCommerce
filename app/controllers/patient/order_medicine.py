from src.services.base_service import BaseService
from flask.views import MethodView
from flask import render_template, request, redirect, url_for

class OrderMedicine(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, patient_service):
        super().__init__()
        self.database_service = database_service
        self.patient_service = patient_service
    
    @BaseService.login_required
    def get(self):
        balance_query = f"SELECT Wallet_balance FROM Patient " +\
                               f"WHERE UID = {self.uid}"
        if self.patient_service.medicines == None:
            medicine_query = f"SELECT * FROM Drug WHERE is_restricted = 0"
            medicine = self.patient_service.fetch_all(query=medicine_query)
        else:
            medicine = self.patient_service.medicines
            self.patient_service.medicines = None
            
        name_query = f"SELECT name FROM User " +\
                               f"WHERE UID = {self.uid}"
        name = self.patient_service.fetch_one(query=name_query)
        name = name["name"]
        
        balance = self.patient_service.fetch_one(query=balance_query)
        
        

        basket_str = ""
        for item in self.patient_service.get_basket():
            print(item)
            basket_str += item["name"] + " - " + str(item["count"]) + ", "
        
        if basket_str != "":
            basket_str = basket_str[:-2]

        total_cost = self.patient_service.cost_basket()

        return render_template("patient/order_medicine_2.html", name=name, balance=balance, medicine=medicine, notifications=self.patient_service.fetch_notifications(self.uid), basket=basket_str, total_cost=total_cost)

    def post(self):
        if "Home" in request.form:
            return redirect(url_for('patient'))
        elif "ordermedicine" in request.form:
            return redirect(url_for("ordermedicine"))
        elif "oldprescriptions" in request.form:
            return redirect(url_for("old_prescriptions"))
        #elif "logout" in request.form:
            #pass
        elif "addbalance" in request.form:
            return redirect(url_for("patient_balance"))
        elif "editprofile" in request.form:
            return redirect(url_for("patient_edit"))
        elif "assistant" in request.form:
            return redirect(url_for('assistant'))
        elif "vieworders" in request.form:
            return redirect(url_for('patient_orders'))
        elif "add" in request.form:
            count = request.form.get("count")
            id = request.form.get("add")
            name = self.patient_service.fetch_one(query=f"SELECT drug_name FROM Drug WHERE drug_id = {id}")
            print(name)
            self.patient_service.add_basket(name["drug_name"], count, id)
            return redirect(url_for("ordermedicine"))
        elif "buy" in request.form:
            self.patient_service.pharmacy_id = None
            return redirect(url_for("select_pharmacy"))
        elif "clear_basket" in request.form:
            self.patient_service.pharmacy_id = None
            self.patient_service.basket = []
            return redirect(url_for("ordermedicine"))
        
        # Medicine search bar(s)
        if "search_name" in request.form:
            name = request.form["search_name"]
            self.patient_service.medicines = self.patient_service.fetch_all(f'SELECT * FROM Drug WHERE drug_name LIKE "%{name}%" AND is_restricted = 0')
            return redirect(url_for("ordermedicine"))
        elif "search_company" in request.form:
            name = request.form["search_company"]
            self.patient_service.medicines = self.patient_service.fetch_all(f'SELECT * FROM Drug WHERE company LIKE "%{name}%" AND is_restricted = 0')
            return redirect(url_for("ordermedicine"))
        elif "search_year" in request.form:
            year = request.form["search_year"]
            if len(year) > 0:
                self.patient_service.medicines = self.patient_service.fetch_all(f'SELECT * FROM Drug WHERE production_year = {year} AND is_restricted = 0')
            return redirect(url_for("ordermedicine"))
        elif "search_class" in request.form:
            name = request.form["search_class"]
            self.patient_service.medicines = self.patient_service.fetch_all(f'SELECT * FROM Drug WHERE drug_class LIKE "%{name}%" AND is_restricted = 0')
            return redirect(url_for("ordermedicine"))
        elif "search_info" in request.form:
            name = request.form["search_info"]
            self.patient_service.medicines = self.patient_service.fetch_all(f'SELECT * FROM Drug WHERE drug_info LIKE "%{name}%" AND is_restricted = 0')
            return redirect(url_for("ordermedicine"))
        elif "search_use_count" in request.form:
            name = request.form["search_use_count"]
            if len(name) > 0:
                self.patient_service.medicines = self.patient_service.fetch_all(f'SELECT * FROM Drug WHERE use_count = {name} AND is_restricted = 0')
            return redirect(url_for("ordermedicine"))
        elif "search_age" in request.form:
            name = request.form["search_age"]
            self.patient_service.medicines = self.patient_service.fetch_all(f'SELECT * FROM Drug WHERE age_group LIKE "%{name}%" AND is_restricted = 0')
            return redirect(url_for("ordermedicine"))
        elif "search_side" in request.form:
            name = request.form["search_side"]
            self.patient_service.medicines = self.patient_service.fetch_all(f'SELECT * FROM Drug WHERE side_effects LIKE "%{name}%" AND is_restricted = 0')
            return redirect(url_for("ordermedicine"))

        
