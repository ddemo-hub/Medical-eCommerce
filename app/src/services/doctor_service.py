from src.utils.singleton import Singleton

from src.services.config_service import ConfigService
import pymysql
import pymysql.cursors

class DoctorService(metaclass=Singleton):
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        self.connection = None

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

    def fetch_one(self, query: str):
        """ Fetch one instance witout specifying columns """
        self.__connect()    
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query=query)
                one = cursor.fetchone()
        except Exception as ex:
            print(f"[ERROR][dql] While executing the query {query}, the following exception raised:\n{ex}")
            return ex
        
        finally:
            self.__disconnect()
            return one
            
    def fetch_all(self, query: str):
        """ Fetch all instances witout specifying columns """
        self.__connect()    
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query=query)
                all = cursor.fetchall()
        except Exception as ex:
            print(f"[ERROR][dql] While executing the query {query}, the following exception raised:\n{ex}")
            return ex
        
        finally:
            self.__disconnect()
            return all
        
    def dml(self, query: str):
        """ Insert, Detele, Update Operations """
        self.__connect()
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query=query)

            self.connection.commit()

        except Exception as ex:
            print(f"[ERROR][dml] While executing the query {query}, the following exception raised:\n{ex}")
            return ex
        
        finally:
            self.__disconnect()
            return 1