from src.utils.singleton import Singleton

from src.services.config_service import ConfigService
import pymysql
import pymysql.cursors

class PatientService(metaclass=Singleton):
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
            return 0
        
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
            return 0
        
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
            return 0
        
        finally:
            self.__disconnect()
            return 1
    
    def fetch_notifications(self, uid: str):
        """ Fetch Notifications """
        notification_query = f"SELECT allow_notifications AS notif FROM Patient WHERE UID = {uid}"
        notification = self.fetch_one(query=notification_query)
        return_arr = []
        if notification["notif"] == 0:
            return return_arr
        reminder_query = f"SELECT D.drug_name as name FROM Assistant_track_Drug ATD NATURAL JOIN Drug D WHERE ATD.Assistant_ID = {uid} AND ATD.Pill_count / ATD.Frequency <= 3 AND ATD.Expiration_date >= CURDATE()"
        exp_query = f"SELECT D.drug_name as name FROM Assistant_track_Drug ATD NATURAL JOIN Drug D WHERE ATD.Assistant_ID = {uid} AND DATE_ADD(CURDATE(), INTERVAL(5) DAY) >= ATD.Expiration_date"
        reminder = self.fetch_all(query=reminder_query)
        expiration = self.fetch_all(query=exp_query)
        for rem in reminder:
            rem_text = rem["name"] + " is about to finish"
            return_arr.append(rem_text) 
        for exp in expiration:
            exp_text =  exp["name"] + "is about to expire"
            return_arr.append(exp_text) 
        return return_arr

        