from flask import Flask
from controllers.doctor.doctor_main import DoctorMain # pycache olusturamadi ;-;

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
    app.add_url_rule("/login", view_func=Login.as_view("login", database_service=app_container.database_service))
    app.add_url_rule("/login_as", view_func=LoginAs.as_view("login_as", database_service=app_container.database_service))
    app.add_url_rule("/register", view_func=Register.as_view("register", database_service=app_container.database_service))
    app.add_url_rule("/register/doctor", view_func=RegisterDoctor.as_view("register_doctor", database_service=app_container.database_service))
    app.add_url_rule("/register/pharmacy", view_func=RegisterPharmacy.as_view("register_pharmacy", database_service=app_container.database_service))
    app.add_url_rule("/register/patient", view_func=RegisterPatient.as_view("register_patient", database_service=app_container.database_service))
    app.add_url_rule("/doctor/main", view_func=DoctorMain.as_view("doctor_main", database_service=app_container.database_service))

    return app

if __name__ == "__main__":
    app = create_app(app_container=AppContainer)
    app.run(debug=False, host=AppContainer.config_service.host, port=AppContainer.config_service.port)
