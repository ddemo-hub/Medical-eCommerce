from src.utils.globals import Globals
from src.utils.singleton import Singleton

from src.services.config_service import ConfigService
from src.services.database_service import DatabaseService
from src.services.patient_service import PatientService
from src.services.doctor_service import DoctorService
from src.services.auth_service import AuthService

from dataclasses import dataclass

@dataclass
class AppContainer(metaclass=Singleton):
    """ The container for all services to be initialized """

    config_service = ConfigService(
        configs=Globals.project_path.joinpath("src", "configs")
    )

    database_service = DatabaseService(config_service=config_service)
    patient_service = PatientService(config_service=config_service)
    doctor_service = DoctorService(config_service=config_service)
    auth_service = AuthService(config_service=config_service)