import mysql.connector

from models.DBConnection import DBConnection
from models.User import User


class Retrait(DBConnection):

    def insert(self, code, amount, date):
        try:
            conn = self.connection()
            print("Connection established:", conn)
        except mysql.connector.Error as error:
            return "Unable to connect to the database: " + str(error)
        if conn:
            cursor = conn.cursor()
            try:

                query = "INSERT INTO retraits (code_user, amount,date) VALUES (%s,%s,%s)"
                values = (code, float(amount), date)
                cursor.execute(query, values)
                conn.commit()


                self.balance = User().select_userById(code)[9]
                total = float(self.balance) - float(amount)


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

    def selectRetraitInfo(self):
            conn = self.connection()
            cursor = conn.cursor()

            # Récupération des données de l'utilisateur
            cursor.execute("SELECT * FROM retraits")
            return cursor.fetchall()

