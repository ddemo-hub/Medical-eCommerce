from .singleton import Singleton

from dataclasses import dataclass
from datetime import datetime 
import pathlib

@dataclass
class Globals(metaclass=Singleton):
    DATETIME_NOW = datetime.now().strftime("%Y_%B/Day_%d/%H.%M.%S")
    
    # Paths
    project_path = pathlib.Path(__file__).parent.parent.parent
    configs_path = project_path.joinpath("src", "configs")
    db_schema_path = project_path.parent.joinpath("db.sql")