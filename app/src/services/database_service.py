from src.utils.singleton import Singleton
from src.utils.globals import Globals

from src.services.config_service import ConfigService

import pymysql
import pandas
import re

class DatabaseService(metaclass=Singleton):
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        self.connection = None

        self.__execute_schema()

    def __execute_schema(self):
        """ 
            Parse .sql file and execute the statements 
            SQL statements must end with a semicolon
        """
        connection = pymysql.connect(
            host=self.config_service.mysql_host,
            user=self.config_service.mysql_user,
            password=self.config_service.mysql_password
        )
        cursor = connection.cursor()

        with open(Globals.db_schema_path, "r") as file:
            schema = file.read()
            statements = schema.split(";")

            for statement in statements:
                statement = re.sub("\n", "", statement)
                try:
                    cursor.execute(f"{statement};")
                    connection.commit()
                except:
                    pass
        
        cursor.close()
        connection.close()

    def __connect(self):
        self.connection = pymysql.connect(
            host=self.config_service.mysql_host,
            user=self.config_service.mysql_user,
            password=self.config_service.mysql_password,
            database=self.config_service.mysql_database
        )

    def __disconnect(self):
        self.connection.close()
        self.connection = None

    def dml(self, query: str):
        """ Insert, Detele, Update Operations """
        result = True
        self.__connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query=query)

            self.connection.commit()

        except Exception as ex:
            print(f"[ERROR][dml] While executing the query {query}, the following exception raised:\n{ex}")
            result = False
        
        finally:
            self.__disconnect()
            return result
        
    def dql(self, query: str, columns: list):
        """ Select Operation """
        self.__connect()    
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query=query)
                records = cursor.fetchall()

                df_table = pandas.DataFrame(records, columns=columns)
                
        except Exception as ex:
            print(f"[ERROR][dql] While executing the query {query}, the following exception raised:\n{ex}")
            return False
        
        finally:
            self.__disconnect()
            return df_table