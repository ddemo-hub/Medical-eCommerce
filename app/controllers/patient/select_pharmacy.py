from src.services.base_service import BaseService
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, session

class SelectPharmacy(MethodView, BaseService):
    init_every_request = True   # Must be set to True for authorization, default is also True

    def __init__(self, database_service, patient_service):
        super().__init__()
        self.database_service = database_service
        self.patient_service = patient_service
    
    @BaseService.login_required
    def get(self):
        balance_query = f"SELECT Wallet_balance FROM Patient " +\
                               f"WHERE UID = {self.uid}"

        suitable_pharmacy_list = []
        pharmacy_query = f"SELECT UID as id, name FROM Pharmacy NATURAL JOIN User"
        pharmacy_list = self.patient_service.fetch_all(query=pharmacy_query)

        for pharmacy in pharmacy_list:
            p_id = pharmacy["id"]
            suitable = 1
            for item in self.patient_service.get_basket():
                med_cnt_query = f"SELECT Count(*) as cnt FROM Inventory WHERE pharmacy_id = {p_id} AND drug_id = {item['id']} AND expiration_date > CURDATE()"
                med_cnt = self.patient_service.fetch_all(query=med_cnt_query)
                for med_cnt in med_cnt:
                    if med_cnt["cnt"] < item["count"]:
                        suitable = 0
            
            if suitable == 1:
                suitable_pharmacy_list.append(pharmacy)

        total_cost = self.patient_service.cost_basket()


        name_query = f"SELECT name FROM User " +\
                               f"WHERE UID = {self.uid}"
        name = self.patient_service.fetch_one(query=name_query)
        name = name["name"]
        
        balance = self.patient_service.fetch_one(query=balance_query)


        return render_template("patient/select_pharmacy.html", name=name, balance=balance, notifications=self.patient_service.fetch_notifications(self.uid), suitable_pharmacy_list=suitable_pharmacy_list, total_cost=total_cost)

    def post(self):
        if "Home" in request.form:
            return redirect(url_for('patient'))
        elif "ordermedicine" in request.form:
            return redirect(url_for("ordermedicine"))
        elif "oldprescriptions" in request.form:
            return redirect(url_for("old_prescriptions"))
        elif "logout" in request.form:
            session.clear()
            session["uid"] = None
            session["logged_in"] = False
            return redirect(url_for('login'))
        elif "addbalance" in request.form:
            return redirect(url_for("patient_balance"))
        elif "editprofile" in request.form:
            return redirect(url_for("patient_edit"))
        elif "assistant" in request.form:
            return redirect(url_for('assistant'))
        elif "vieworders" in request.form:
            return redirect(url_for('patient_orders'))
        elif "buy_delivery" in request.form:
            self.patient_service.order_basket(self.uid, request.form.get("buy_delivery"), self.patient_service.pharmacy_id, "on_delivery")
            self.patient_service.message = "Order Successful"
            return redirect(url_for('patient'))
        elif "buy_balance" in request.form:
            balance_query = f"SELECT Wallet_balance FROM Patient " +\
                        f"WHERE UID = {self.uid}"
            balance = self.patient_service.fetch_one(query=balance_query)
            total_cost = self.patient_service.cost_basket()
            if int(total_cost) > int(balance["Wallet_balance"]):
                self.patient_service.message = "Order Failed"
                return redirect(url_for('patient'))
            else:
                self.patient_service.order_basket(self.uid, request.form.get("buy_balance"), self.patient_service.pharmacy_id, "balance")
                self.patient_service.message = "Order Successful"
                return redirect(url_for('patient'))

        
