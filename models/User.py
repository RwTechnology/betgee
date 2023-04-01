from models.DBConnection import DBConnection
import mysql.connector
import hashlib


class User(DBConnection):

    def add_account(self, code, last_name, first_name, username, date_of_birth, gender, phone, nif_cin, password,
                    balance,
                    status, user_type):
        conn = self.connection()
        if conn:
            cursor = conn.cursor()
            password_hash = password
            try:
                query = "INSERT INTO users (id, last_name, first_name, username, date_of_birth, gender, phone, nif_cin, password, balance, status, user_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (
                    code, last_name, first_name, username, date_of_birth, gender, phone, nif_cin, password_hash,
                    balance,
                    status, user_type)
                cursor.execute(query, values)
                conn.commit()
                return "add_success"

            except mysql.connector.Error as error:
                return "Impossible d'insérer les données dans la BD" + str(error)
            finally:
                cursor.close()
                conn.close()

    def update_account(self, last_name, first_name, username, date_of_birth, gender, phone, nif_cin, code):
        conn = self.connection()
        if conn:
            cursor = conn.cursor()
            try:
                query = "UPDATE users SET last_name=%s, first_name=%s, username=%s, date_of_birth=%s, gender=%s, phone=%s, nif_cin=%s WHERE id=%s"
                values = (
                    last_name, first_name, username, date_of_birth, gender, phone, nif_cin, code)
                cursor.execute(query, values)
                conn.commit()
                return "update_success"
            except mysql.connector.Error as error:
                return "Impossible d'insérer les données dans la BD" + str(error)
            finally:
                cursor.close()
                conn.close()

    def update_password(self, password, code):
        conn = self.connection()
        if conn:
            cursor = conn.cursor()
            try:
                query = "UPDATE users SET password=%s WHERE id=%s"
                values = (password, code)
                cursor.execute(query, values)
                conn.commit()
                return "update_success"
            except mysql.connector.Error as error:
                return "Impossible d'insérer les données dans la BD" + str(error)
            finally:
                cursor.close()
                conn.close()

    def login(self, username, password):
        conn = self.connection()
        cursor = conn.cursor()
        password_hash = password
        try:
            # Récupération de toutes les données de l'utilisateur
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password_hash))
            user_data = cursor.fetchone()

            if user_data:
                # Les données de l'utilisateur ont été trouvées
                if user_data[10] == 'inactive':
                    return 'inactive'
                elif user_data[10] == 'delete':
                    return 'delete'
                else:
                    self.truncate_userAuth()
                    self.insert_userAuth(user_data[0])
                    # Enregistrement des modifications
                    conn.commit()
                    return 'valid'
            else:
                # Les données de l'utilisateur n'ont pas été trouvées
                return False
        except mysql.connector.Error as error:
            return False
        finally:
            cursor.close()

    def selectUserInfo(self):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    def select_userById(self, user_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur avec l'ID donné
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_code,))
        return cursor.fetchone()

    def check_username(self, username):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur avec l'ID donné
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            return True
        else:
            return False

    def check_phone(self, phone):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur avec l'ID donné
        cursor.execute("SELECT * FROM users WHERE phone=%s", (phone,))
        if cursor.fetchone():
            return True
        else:
            return False

    def check_nif_cin(self, nif_cin):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur avec l'ID donné
        cursor.execute("SELECT * FROM users WHERE nif_cin=%s", (nif_cin,))
        if cursor.fetchone():
            return True
        else:
            return False

    def selectUserByIdMany(self, user_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur avec l'ID donné
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_code,))
        return cursor.fetchmany()


    def insert_userAuth(self, code_user):
        conn = self.connection()
        cursor = conn.cursor()

        # Insertion des données de l'utilisateur dans la table user_auth
        cursor.execute("INSERT INTO user_auth (code_user) VALUES (%s)", (code_user,))

        # Enregistrement des modifications
        conn.commit()

    def truncate_userAuth(self):
        conn = self.connection()
        cursor = conn.cursor()

        # Suppression de toutes les données de la table user_auth
        cursor.execute("TRUNCATE TABLE user_auth")

        # Enregistrement des modifications
        conn.commit()

    def display_UserAuth(self):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération de toutes les données de la table user_auth
        cursor.execute("SELECT * FROM user_auth")
        rows = cursor.fetchall()

        if rows:
            return rows[0][1]
        else:
            return False
