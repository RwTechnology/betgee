from models.DBConnection import DBConnection
import mysql.connector


class Payment(DBConnection):

    def insert(self,bet_code,payment_date,montant_payment):
        try:
            conn = self.connection()
            print("Connection established:", conn)
        except mysql.connector.Error as error:
            return "Unable to connect to the database: " + str(error)

        if conn:
            cursor = conn.cursor()
            try:
                query = "INSERT INTO payments (bet_code,payment_date,montant_payment) VALUES (%s,%s,%s)"
                values = (bet_code,payment_date,montant_payment)
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

    def selectPaymentInfo(self):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur
        cursor.execute("SELECT * FROM payments")
        return cursor.fetchall()