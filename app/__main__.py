from flask import Flask
from flask_apscheduler import APScheduler

from controllers import *

from src.containers.app_container import AppContainer

def create_app(app_container: AppContainer) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = app_container.config_service.secret_key
    
    app.add_url_rule("/pharmacy", view_func=PharmacyMain.as_view("pharmacy_main", database_service=app_container.database_service))
    app.add_url_rule("/patient_main", view_func=PatientMain.as_view("patient", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/oldprescriptions", view_func=OldPrescriptions.as_view("old_prescriptions", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/patientbalance", view_func=PatientBalance.as_view("patient_balance", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/patientedit", view_func=PatientEdit.as_view("patient_edit", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/assistant", view_func=Assistant.as_view("assistant", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/patientorder", view_func=PatientOrders.as_view("patient_orders", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/login",              view_func=Login.as_view("login", database_service=app_container.database_service))
    app.add_url_rule("/login_as",           view_func=LoginAs.as_view("login_as", database_service=app_container.database_service))
    app.add_url_rule("/register",           view_func=Register.as_view("register", database_service=app_container.database_service))
    app.add_url_rule("/register/doctor",    view_func=RegisterDoctor.as_view("register_doctor", database_service=app_container.database_service))
    app.add_url_rule("/register/pharmacy",  view_func=RegisterPharmacy.as_view("register_pharmacy", database_service=app_container.database_service))
    app.add_url_rule("/register/patient",   view_func=RegisterPatient.as_view("register_patient", database_service=app_container.database_service))
    app.add_url_rule("/doctor/main",                    view_func=DoctorMain.as_view("doctor_main", database_service=app_container.database_service,doctor_service=app_container.doctor_service))
    app.add_url_rule("/doctor/add_prescription",        view_func=AddPrescription.as_view("add_prescription", database_service=app_container.database_service,doctor_service=app_container.doctor_service))
    app.add_url_rule("/doctor/add_medicine_to_presc",   view_func=AddMedicineToPrescription.as_view("add_medicine_to_prescription", database_service=app_container.database_service,doctor_service=app_container.doctor_service))
    app.add_url_rule("/doctor/past_prescriptions",      view_func=DoctorPastPrescriptions.as_view("doctor_past_prescriptions", database_service=app_container.database_service,doctor_service=app_container.doctor_service))
    app.add_url_rule("/doctor/prescription_details",    view_func=DoctorViewPrescriptionDetails.as_view("doctor_view_prescription_details", database_service=app_container.database_service,doctor_service=app_container.doctor_service))
    app.add_url_rule("/doctor/medicines",               view_func=DoctorListMedicines.as_view("doctor_list_medicines", database_service=app_container.database_service,doctor_service=app_container.doctor_service))

    return app 

def update_prescription_validation():
    AppContainer.database_service.dml("UPDATE db.prescription SET is_valid = 0 WHERE CURDATE() > expiration_date")

if __name__ == "__main__":
    app = create_app(app_container=AppContainer)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='test-job', func=update_prescription_validation, trigger='interval', seconds=60)

    app.run(debug=True, host=AppContainer.config_service.host, port=AppContainer.config_service.port)

    