from models.DBConnection import DBConnection
import mysql.connector


class Match(DBConnection):

    def insert(self, code,match_type, country, match_date, match_time, receiver_team, visitor_team, cote_match, score, state):
        try:
            conn = self.connection()
            print("Connection established:", conn)
        except mysql.connector.Error as error:
            return "Unable to connect to the database: " + str(error)

        if conn:
            cursor = conn.cursor()
            try:
                query = "INSERT INTO matchs (id,match_type, country, match_date, match_time, receiver_team, visitor_team, cote_match, score, state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (code,match_type, country, match_date, match_time, receiver_team, visitor_team, cote_match, score, state)
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



    def update(self,match_type, country, match_date, match_time, receiver_team, visitor_team, cote_match,
                   score,
                   state, id):
            try:
                conn = self.connection()
                print("Connection established:", conn)
            except mysql.connector.Error as error:
                return "Unable to connect to the database: " + str(error)

            if conn:
                cursor = conn.cursor()
                try:
                    query = "UPDATE matchs SET match_type=%s,country=%s,match_date=%s,match_time=%s,receiver_team=%s,visitor_team=%s,cote_match=%s,score=%s,state=%s WHERE id=%s"
                    values = (match_type, country, match_date, match_time, receiver_team, visitor_team, cote_match, score, state, id)
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


    def selectMatchInfo(self):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur
        cursor.execute("SELECT * FROM matchs")
        return cursor.fetchall()


    def selectMatchNotPlayInfo(self):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur
        cursor.execute("SELECT * FROM matchs WHERE state = 'N'")
        return cursor.fetchall()

    def selectMatchById(self, match_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur avec l'ID donné
        cursor.execute("SELECT * FROM matchs WHERE id=%s", (match_code,))
        match = cursor.fetchone()

        if match is None:
            # Cas ou aucun match n'est trouvé avec le code donné
            print("Aucun match trouvé avec le code '{}'".format(match_code))
            return None
        else:
            return match

    def selectMatchByIdMany(self, match_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données de l'utilisateur avec l'ID donné
        cursor.execute("SELECT * FROM matchs WHERE id=%s", (match_code,))
        match = cursor.fetchmany()

        if match is None:
            # Cas ou aucun match n'est trouvé avec le code donné
            print("Aucun match trouvé avec le code '{}'".format(match_code))
            return None
        else:
            return match

    def deleteMatch(self, match_code):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM matchs WHERE id=%s", (match_code,))
        # Enregistrement des modifications
        conn.commit()
