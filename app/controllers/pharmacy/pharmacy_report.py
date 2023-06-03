from src.services.base_service import BaseService
from src.services.database_service import DatabaseService
from src.services.pharmacy_service import PharmacyService

from flask import render_template
from flask.views import MethodView


class PharmacyReport(MethodView, BaseService, DatabaseService, PharmacyService):
    def __init__(self, database_service, pharmacy_service):
        super().__init__()
        self.pharmacy_service = pharmacy_service
        self.database_service = database_service

    @BaseService.login_required
    def get(self):
        sales_last_month = f"SELECT count(*) AS count from drug_order WHERE pharmacy_id = {self.uid} AND date >= " \
                           f"DATE_SUB(NOW(), INTERVAL 1 MONTH);"
        drugs_sold = f"SELECT Pharmacy.UID, Pharmacy.address, COUNT(DISTINCT Order_Contains_Drug.drug_id) AS " \
                     f"drug_count FROM Pharmacy JOIN Drug_Order ON Pharmacy.UID = Drug_Order.pharmacy_id JOIN " \
                     f"Order_Contains_Drug ON Drug_Order.order_id = Order_Contains_Drug.order_id WHERE " \
                     f"Drug_Order.order_status = 'completed' GROUP BY Pharmacy.UID, Pharmacy.address;"
        drug_count = f"SELECT Drug.drug_id, Drug.drug_name, COUNT(*) AS sold_count FROM Drug JOIN Order_Contains_Drug " \
                     f"ON Drug.drug_id = Order_Contains_Drug.drug_id JOIN Drug_Order ON Order_Contains_Drug.order_id " \
                     f"= Drug_Order.order_id WHERE Drug_Order.order_status = 'completed' GROUP BY Drug.drug_id, " \
                     f"Drug.drug_name;"
        most_sold_drug = f"SELECT Drug.drug_id, Drug.drug_name, SUM(Order_Contains_Drug.count) AS total_sold FROM " \
                         f"Drug JOIN Order_Contains_Drug ON Drug.drug_id = Order_Contains_Drug.drug_id JOIN " \
                         f"Drug_Order ON Order_Contains_Drug.order_id = Drug_Order.order_id WHERE " \
                         f"Drug_Order.order_status = 'completed' GROUP BY Drug.drug_id, Drug.drug_name ORDER BY " \
                         f"total_sold DESC LIMIT 1;"
        price_last_week = f"SELECT SUM(Drug.price * Order_Contains_Drug.count) AS total_price FROM Drug JOIN " \
                          f"Order_Contains_Drug ON Drug.drug_id = Order_Contains_Drug.drug_id JOIN Drug_Order ON " \
                          f"Order_Contains_Drug.order_id = Drug_Order.order_id WHERE Drug_Order.order_status = " \
                          f"'completed' AND Drug_Order.date >= DATE_SUB(NOW(), INTERVAL 1 WEEK);"
        total_profit = f"SELECT SUM(total_price) AS total_revenue FROM Drug_Order WHERE order_status = 'completed';"
        total_patients = f"SELECT COUNT(*) AS total_patients FROM Patient;"
        total_prescriptions = f"SELECT COUNT(*) AS total_prescriptions FROM Prescription;"
        avg_drug_price = f"SELECT AVG(price) AS average_price FROM Drug;"
        avg_order_price = f"SELECT AVG(total_price) AS average_order_price FROM Drug_Order WHERE order_status = " \
                          f"'completed';"

        self.pharmacy_service.fetch_all(query=sales_last_month)
        self.pharmacy_service.fetch_all(query=drugs_sold)
        self.pharmacy_service.fetch_all(query=most_sold_drug)
        self.pharmacy_service.fetch_all(query=drug_count)
        self.pharmacy_service.fetch_all(query=price_last_week)
        self.pharmacy_service.fetch_all(query=total_profit)
        self.pharmacy_service.fetch_all(query=total_patients)
        self.pharmacy_service.fetch_all(query=total_prescriptions)
        self.pharmacy_service.fetch_all(query=avg_drug_price)
        self.pharmacy_service.fetch_all(query=avg_order_price)

        return render_template("pharmacy_report.html", sales_last_month=sales_last_month, drugs_sold=drugs_sold,
                               most_sold_drug=most_sold_drug, drug_count=drug_count,
                               price_last_week=price_last_week, total_profit=total_profit,
                               total_patients=total_patients, total_prescriptions=total_prescriptions,
                               avg_drug_price=avg_drug_price, avg_order_price=avg_order_price)
