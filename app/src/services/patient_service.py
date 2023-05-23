from src.utils.singleton import Singleton

from src.services.config_service import ConfigService
import pymysql
import pymysql.cursors

class PatientService(metaclass=Singleton):
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        self.connection = None
        self.basket = []
        self.pharmacy_id = None
        self.message = None

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
        reminder_query = f"SELECT D.drug_name as name FROM Assistant_track_Drug ATD NATURAL JOIN Drug D WHERE ATD.Assistant_ID = {uid} AND ATD.Pill_count * ATD.Frequency <= 3 AND ATD.Expiration_date >= CURDATE()"
        exp_query = f"SELECT D.drug_name as name FROM Assistant_track_Drug ATD NATURAL JOIN Drug D WHERE ATD.Assistant_ID = {uid} AND DATE_ADD(CURDATE(), INTERVAL(5) DAY) >= ATD.Expiration_date"
        reminder = self.fetch_all(query=reminder_query)
        expiration = self.fetch_all(query=exp_query)
        for rem in reminder:
            rem_text = rem["name"] + " is about to finish"
            return_arr.append(rem_text) 
        for exp in expiration:
            exp_text =  exp["name"] + " is about to expire"
            return_arr.append(exp_text) 
        return return_arr
    
    def get_basket(self):
        return self.basket
    
    def add_basket(self, name, count, id):
        item = {
            "name": name,
            "count": int(count),
            "id": id
        }
        for med in self.basket:
            if med["id"] == id:
                med["count"] += int(count)
                return
        self.basket.append(item)
    
    def cost_basket(self):
        total_cost = 0
        for item in self.basket:
            medicine = self.fetch_one(query=f"SELECT price FROM Drug WHERE drug_id = {item['id']}")
            total_cost += (int(medicine["price"]) * int(item["count"]))
        return total_cost
    
    def order_basket(self, patient_id, pharmacy_id, prescription, method):
        method = "\"" + method + "\""
            #order_id = self.fetch_one(query=f"SELECT order_id FROM Prescription WHERE prescription_id = {prescription}")
            #order_id = order_id['order_id']
            #order_query = f"UPDATE Drug_Order SET date = CURDATE(), payment_method = {method}, total_price ={self.cost_basket()}, order_status = 1, pharmacy_id = {pharmacy_id} WHERE order_id = {order_id}"
            #self.dml(order_query)
        order_query = f"INSERT INTO Drug_Order VALUES (NULL, CURDATE(), {method}, {self.cost_basket()}, 1, {patient_id}, {pharmacy_id})"
        self.dml(order_query)
        order_id_query = f"SELECT MAX(order_id) as id FROM Drug_Order"
        order_id = self.fetch_one(query=order_id_query)
        order_id = order_id['id']
        if prescription != None:
            self.pharmacy_id = None
            self.dml(f"UPDATE Prescription SET is_valid = 0, order_id = {order_id} WHERE prescription_id = {prescription}")
        else:
            prescription = "NULL"
        for item in self.get_basket():
            use_count = self.fetch_one(f"SELECT use_count FROM Drug WHERE drug_id = {item['id']}")
            print(use_count)
            pill_count = int(item['count']) * int(use_count['use_count'])
            drug_query = f"INSERT INTO Order_Contains_Drug VALUES ({order_id}, {item['id']}, {prescription}, {item['count']})"
            self.dml(drug_query)
            inventory_query = f"SELECT * FROM Inventory WHERE pharmacy_id = {pharmacy_id} AND drug_id = {item['id']} AND expiration_date > CURDATE() ORDER BY expiration_date LIMIT {item['count']}"
            inventory_delete_query = f"DELETE FROM Inventory WHERE pharmacy_id = {pharmacy_id} AND drug_id = {item['id']} AND expiration_date > CURDATE() ORDER BY expiration_date LIMIT {item['count']}"
            inventory = self.fetch_all(inventory_query)
            self.dml(inventory_delete_query)
            exp_date = "\"" + str(inventory[0]['expiration_date'].date()) + "\""

            if self.check_assistant(patient_id, item['id']):
                assistant_query = f'INSERT INTO Assistant_track_Drug (`Assistant_ID`, `Drug_ID`, `Count`, `Frequency`, `Expiration_date`, `Last_time_taken`, `Pill_count`) VALUES ({patient_id}, {item["id"]}, {item["count"]}, 1, {exp_date}, CURDATE(), {pill_count})'
            else:
                assistant_query = f'UPDATE Assistant_track_Drug SET Count = Count + {item["count"]}, Expiration_date = {exp_date}, Pill_count = Pill_count + {pill_count} WHERE Assistant_ID = {patient_id} AND Drug_ID = {item["id"]}'
            self.dml(assistant_query)

        if method == "\"balance\"":
            balance_query = f"SELECT Wallet_balance FROM Patient " +\
                               f"WHERE UID = {patient_id}"
            balance = self.fetch_one(query=balance_query)
            newbalance = balance["Wallet_balance"] - int(self.cost_basket())
            print(self.cost_basket())
            print(newbalance)
            balance_update_query = f"UPDATE Patient SET Wallet_balance = {newbalance} WHERE UID = {patient_id}"
            self.dml(balance_update_query)

        self.basket = []

    def check_assistant(self, patient_id, drug_id):
        query = f"SELECT COUNT(*) AS cnt FROM Assistant_track_Drug WHERE Assistant_ID = {patient_id} AND Drug_ID = {drug_id}"
        count = self.fetch_one(query=query)
        count= count["cnt"]
        if int(count) > 0:
            return False
        else:
            return True
        
            

        



        