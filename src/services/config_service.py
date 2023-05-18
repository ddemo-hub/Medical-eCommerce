from src.utils.singleton import Singleton

import pathlib
import uuid
import yaml 
import os

class ConfigService(metaclass=Singleton):
    def __init__(self, configs: pathlib.Path):
        self.config = {} 

        # Append the contents of every .yaml file in configs directory into self.config dictionary 
        for config_file in os.listdir(configs):
            config_name = config_file[:-5]  # Remove .yaml suffix
            config_path = configs.joinpath(config_file) 
            
            with open(config_path, "r") as cf:
                self.config[config_name] = yaml.safe_load(cf)

    @property
    def secret_key(self):
        secret_key = self.config["server"]["secret_key"]
        return secret_key if secret_key is not None else uuid.uuid4().hex

    @property
    def host(self):
        return self.config["server"]["host"]

    @property
    def port(self):
        return self.config["server"]["port"]

    @property
    def mysql_host(self):
        return self.config["connection"]["mysql"]["host"]
    
    @property
    def mysql_user(self):
        return self.config["connection"]["mysql"]["user"]
    
    @property
    def mysql_password(self):
        return self.config["connection"]["mysql"]["password"]
    
    @property
    def mysql_database(self):
        return self.config["connection"]["mysql"]["database"]
