from models.DBConnection import DBConnection
import mysql.connector
from models.User import User


class RechargeAccount(DBConnection):

    def insert(self, code, amount, date):
        try:
            conn = self.connection()
            print("Connection established:", conn)
        except mysql.connector.Error as error:
            return "Unable to connect to the database: " + str(error)
        if conn:
            cursor = conn.cursor()
            try:

                query = "INSERT INTO credits (code_user, amount,date) VALUES (%s,%s,%s)"
                values = (code, float(amount), date)
                cursor.execute(query, values)
                conn.commit()


                self.balance = User().select_userById(code)[9]
                total = float(self.balance) + float(amount)


                query = "UPDATE users SET balance=%s WHERE id=%s"
                values = (total, code)
                cursor.execute(query, values)
                conn.commit()

                return "add_success"
            except mysql.connector.Error as error:
                print("Error executing query:", error)
                return "Unable to update or insert data in the database: " + str(error)
            finally:
                cursor.close()
                conn.close()
        else:
            return "Unable to connect to the database"


    def updateBalance(self, code, amount):
        try:
            conn = self.connection()
            print("Connection established:", conn)
        except mysql.connector.Error as error:
            return "Unable to connect to the database: " + str(error)
        if conn:
            cursor = conn.cursor()
            try:

                query = "UPDATE users SET balance=%s WHERE id=%s"
                values = (amount, code)
                cursor.execute(query, values)
                conn.commit()

                return "update_success"
            except mysql.connector.Error as error:
                print("Error executing query:", error)
                return "Unable to update or insert data in the database: " + str(error)
            finally:
                cursor.close()
                conn.close()
        else:
            return "Unable to connect to the database"


    def selectCreditInfo(self):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage
        cursor.execute("SELECT * FROM credits")
        return cursor.fetchall()

    def selectCreditById(self, credit_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage avec l'ID donné
        cursor.execute("SELECT * FROM credits WHERE id=%s", (credit_code,))
        match = cursor.fetchone()
        if match is None:
            # Cas ou aucun pariage n'est trouvé avec le code donné
            print("Aucun match trouvé avec le code '{}'".format(credit_code))
            return None
        else:
            return match

    def selectCreditInfoById(self, credit_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage avec l'ID donné
        cursor.execute("SELECT * FROM bets WHERE account_id=%s", (credit_code,))
        match = cursor.fetchone()
        if match is None:
            # Cas ou aucun pariage n'est trouvé avec le code donné
            print("Aucun pariage trouvé avec le code '{}'".format(credit_code))
            return None
        else:
            return match

    def selectRechargeInfo(self):
            conn = self.connection()
            cursor = conn.cursor()

            # Récupération des données de l'utilisateur
            cursor.execute("SELECT * FROM credits")
            return cursor.fetchall()





