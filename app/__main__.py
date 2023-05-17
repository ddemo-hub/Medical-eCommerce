from flask import Flask

from controllers import *

from src.containers.app_container import AppContainer

def create_app(app_container: AppContainer) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = app_container.config_service.secret_key
    
    app.add_url_rule("/pharmacy", view_func=PharmacyMain.as_view("pharmacy", database_service=app_container.database_service))
    app.add_url_rule("/patientmain", view_func=PatientMain.as_view("patient", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/oldprescriptions", view_func=OldPrescriptions.as_view("old_prescriptions", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/patientbalance", view_func=PatientBalance.as_view("patient_balance", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/patientedit", view_func=PatientEdit.as_view("patient_edit", database_service=app_container.database_service, patient_service=app_container.patient_service))
    app.add_url_rule("/assistant", view_func=Assistant.as_view("assistant", database_service=app_container.database_service, patient_service=app_container.patient_service))
    
    return app

if __name__ == "__main__":
    app = create_app(app_container=AppContainer)
    app.run(host=AppContainer.config_service.host, port=AppContainer.config_service.port)
