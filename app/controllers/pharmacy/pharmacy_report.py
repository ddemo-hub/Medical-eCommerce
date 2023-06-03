from src.services.base_service import BaseService
from src.services.database_service import DatabaseService
from src.services.pharmacy_service import PharmacyService

from flask.views import MethodView
from flask import Flask, render_template, request, redirect, url_for, session


class PharmacyReport(MethodView, BaseService, DatabaseService, PharmacyService):
    def __init__(self, database_service, pharmacy_service):
        super().__init__()
        self.pharmacy_service = pharmacy_service
        self.database_service = database_service

    @BaseService.login_required
    def get(self):
        sales_last_monthQ = f"SELECT count(*) AS count from drug_order WHERE pharmacy_id = {self.uid} AND date >= " \
                           f"DATE_SUB(NOW(), INTERVAL 1 MONTH);"
        drugs_soldQ = f"SELECT Pharmacy.UID, Pharmacy.address, COUNT(DISTINCT Order_Contains_Drug.drug_id) AS " \
                     f"drug_count FROM Pharmacy JOIN Drug_Order ON Pharmacy.UID = Drug_Order.pharmacy_id JOIN " \
                     f"Order_Contains_Drug ON Drug_Order.order_id = Order_Contains_Drug.order_id WHERE " \
                     f"Drug_Order.order_status = 'completed' GROUP BY Pharmacy.UID, Pharmacy.address;"
        drug_countQ = f"SELECT Drug.drug_id, Drug.drug_name, COUNT(*) AS sold_count FROM Drug JOIN Order_Contains_Drug " \
                     f"ON Drug.drug_id = Order_Contains_Drug.drug_id JOIN Drug_Order ON Order_Contains_Drug.order_id " \
                     f"= Drug_Order.order_id WHERE Drug_Order.order_status = 'completed' GROUP BY Drug.drug_id, " \
                     f"Drug.drug_name;"
        most_sold_drugQ = f"SELECT Drug.drug_id, Drug.drug_name, SUM(Order_Contains_Drug.count) AS total_sold FROM " \
                         f"Drug JOIN Order_Contains_Drug ON Drug.drug_id = Order_Contains_Drug.drug_id JOIN " \
                         f"Drug_Order ON Order_Contains_Drug.order_id = Drug_Order.order_id WHERE " \
                         f"Drug_Order.order_status = 'completed' GROUP BY Drug.drug_id, Drug.drug_name ORDER BY " \
                         f"total_sold DESC LIMIT 1;"
        price_last_weekQ = f"SELECT SUM(Drug.price * Order_Contains_Drug.count) AS total_price FROM Drug JOIN " \
                          f"Order_Contains_Drug ON Drug.drug_id = Order_Contains_Drug.drug_id JOIN Drug_Order ON " \
                          f"Order_Contains_Drug.order_id = Drug_Order.order_id WHERE Drug_Order.order_status = " \
                          f"'completed' AND Drug_Order.date >= DATE_SUB(NOW(), INTERVAL 1 WEEK);"
        total_profitQ = f"SELECT SUM(total_price) AS total_revenue FROM Drug_Order WHERE order_status = 'completed';"
        total_patientsQ = f"SELECT COUNT(*) AS total_patients FROM Patient;"
        total_prescriptionsQ = f"SELECT COUNT(*) AS total_prescriptions FROM Prescription;"
        avg_drug_priceQ = f"SELECT AVG(price) AS average_price FROM Drug;"
        avg_order_priceQ = f"SELECT AVG(total_price) AS average_order_price FROM Drug_Order WHERE order_status = " \
                          f"'completed';"

        sales_last_month = self.pharmacy_service.fetch_one(query=sales_last_monthQ)
        sales_last_month = sales_last_month["count"]
        drugs_sold = self.pharmacy_service.fetch_one(query=drugs_soldQ)
        most_sold_drug = self.pharmacy_service.fetch_one(query=most_sold_drugQ)
        drug_count = self.pharmacy_service.fetch_one(query=drug_countQ)
        price_last_week = self.pharmacy_service.fetch_one(query=price_last_weekQ)
        price_last_week = price_last_week["total_price"]
        total_profit = self.pharmacy_service.fetch_one(query=total_profitQ)
        total_profit = total_profit["total_revenue"]
        total_patients = self.pharmacy_service.fetch_one(query=total_patientsQ)
        total_patients = total_patients["total_patients"]
        total_prescriptions = self.pharmacy_service.fetch_one(query=total_prescriptionsQ)
        total_prescriptions = total_prescriptions["total_prescriptions"]
        avg_drug_price = self.pharmacy_service.fetch_one(query=avg_drug_priceQ)
        avg_drug_price = avg_drug_price["average_price"]
        avg_order_price = self.pharmacy_service.fetch_one(query=avg_order_priceQ)
        avg_order_price = avg_order_price["average_order_price"]

        return render_template("pharmacy/pharmacy_report.html", sales_last_month=sales_last_month, drugs_sold=drugs_sold,
                               most_sold_drug=most_sold_drug, drug_count=drug_count,
                               price_last_week=price_last_week, total_profit=total_profit,
                               total_patients=total_patients, total_prescriptions=total_prescriptions,
                               avg_drug_price=avg_drug_price, avg_order_price=avg_order_price)

    def post(self):
        message = ''

        if "Home" in request.form:
            return redirect(url_for('pharmacy_main'))
        if "vieworders" in request.form:
            return redirect(url_for("pharmacy_orders"))
        if "logout" in request.form:
            session.clear()
            session["uid"] = None
            session["logged_in"] = False
            return redirect(url_for('login'))