from typing import List, Tuple

from models.DBConnection import DBConnection
import mysql.connector

from models.Match import Match
from models.User import User


class Bet(DBConnection):

    def insert(self,code_pariage,account_id,bet_date,bet_amount):
        try:
            conn = self.connection()
            print("Connection established:", conn)
        except mysql.connector.Error as error:
            return "Unable to connect to the database: " + str(error)

        if conn:
            cursor = conn.cursor()
            try:
                query = "INSERT INTO bets (code_pariage,account_id,bet_date,bet_amount) VALUES (%s,%s,%s,%s)"
                values = (code_pariage, account_id, bet_date, float(bet_amount))
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

    def insert_mach_choisie(self, code_pariage, id_match, equipe_choisie, cote, score_prevu, etat_pariage):
        try:
            conn = self.connection()
            print("Connection established:", conn)
        except mysql.connector.Error as error:
            return "Unable to connect to the database: " + str(error)

        if conn:
            cursor = conn.cursor()
            try:
                query = "INSERT INTO match_choisi (code_pariage, id_match, equipe_choisie, cote, score_prevu, etat_pariage) VALUES (%s,%s,%s,%s,%s,%s)"
                values = (code_pariage, id_match, equipe_choisie, cote, score_prevu, etat_pariage)
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

    def update(self, account_id, match_id, bet_date, bet_amount, bet_score, id):
        try:
            conn = self.connection()
            print("Connection established:", conn)
        except mysql.connector.Error as error:
            return "Unable to connect to the database: " + str(error)

        if conn:
            cursor = conn.cursor()
            try:
                query = "UPDATE bets SET account_id=%s,match_id=%s,bet_date=%s,bet_amount=%s,bet_score=%s WHERE id=%s"
                values = (account_id, match_id, bet_date, float(bet_amount), bet_score, id)
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

    def selectBetInfo(self):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage
        cursor.execute("SELECT * FROM bets")
        return cursor.fetchall()

    def selectAmountBetById(self, bet_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage avec l'ID donné
        cursor.execute("SELECT * FROM bets WHERE id=%s", (bet_code,))
        match = cursor.fetchone()
        if match is None:
            # Cas ou aucun pariage n'est trouvé avec le code donné
            print("Aucun match trouvé avec le code '{}'".format(bet_code))
            return None
        else:
            return match

    def selectBetById(self, bet_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage avec l'ID donné
        cursor.execute("SELECT * FROM bets WHERE id=%s", (bet_code,))
        match = cursor.fetchone()
        if match is None:
            # Cas ou aucun pariage n'est trouvé avec le code donné
            print("Aucun match trouvé avec le code '{}'".format(bet_code))
            return None
        else:
            return match

    def selectBetByUserId(self, user_code):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage avec l'ID donné
        cursor.execute("SELECT * FROM bets WHERE account_id=%s", (user_code,))
        match = cursor.fetchall()
        if match is None:
            # Cas ou aucun pariage n'est trouvé avec le code donné
            print("Aucun pariage trouvé avec le code '{}'".format(user_code))
            return None
        else:
            return match

    def displayMatchByBetCode(self, code_pariage):
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du match avec le code de pariage donné
        cursor.execute("SELECT * FROM match_choisi WHERE code_pariage=%s", (code_pariage,))
        return cursor.fetchall()

    def deleteBet(self, bet_code):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bets WHERE id=%s", (bet_code,))
        # Enregistrement des modifications
        conn.commit()

    def list_winning_bets(self,user_id: int) -> List[Tuple[int, int, float]]:

        winning_bets = []

        # Vérifiez si l'ID de l'utilisateur est valide
        if not self.user_exists(user_id):
            raise ValueError("L'ID de l'utilisateur est incorrect.")

        # Récupérez les paris sportifs du joueur d'ID user_id
        bets = Bet().selectBetByUserId(user_id)

        # Parcourez chaque pari et vérifiez s'il a gagné
        for bet in bets:
            bet_id = bet[0]
            match_id = bet[1]
            bet_amount = bet[2]
            bet_score = bet[3]

            # Vérifiez si le match a un gagnant déterminé
            if not self.match_has_winner(match_id):
                continue

            # Vérifiez si le pari du joueur est gagnant
            if self.is_winning_bet(match_id, bet_score):
                # Ajoutez le pari à la liste des paris gagnants
                winning_bets.append((bet_id, match_id, bet_amount))

        return winning_bets


    def user_exists(self, user_id: int) -> bool:

        user = User().select_userById(user_id)
        if user is None:
            return False
        return True

    def user_exists(self,user_id: int) -> bool:

        # Vérifiez si l'ID de l'utilisateur est présent dans la base de données
        if user_id not in [1, 2, 3]:
            raise ValueError("L'ID de l'utilisateur est incorrect.")
        return True

    def is_winning_bet(self,match_id: int, bet_score: str) -> bool:

        match_score = Match().selectMatchById(match_id)
        # Vérifiez si le score du pari du joueur correspond au score du match
        if bet_score != match_score:
            raise ValueError("Le pari du joueur n'est pas gagnant.")
        return True

    def pay_winning_bets(self,user_id: int):

        # Récupérez la liste des paris gagnants de l'utilisateur
        winning_bets = self.list_winning_bets(user_id)
        # Pour chaque pari gagnant de l'utilisateur
        for bet in winning_bets:
            bet_id, match_id, bet_amount = bet
            # Payez le pari
            self.pay_bet(bet_id, bet_amount)


    def pay_bet(self,bet_id: int, amount: int):

        # Récupérez les informations du pari à payer
        bet_info = Bet().selectBetById(bet_id)
        bet_user_id, bet_match_id, bet_score, bet_amount = bet_info
            # Vérifiez si l'ID du pari est valide
        if not self.bet_exists(bet_id):
            raise ValueError("L'ID du pari est incorrect.")
        # Vérifiez si le montant du pari est valide
        if bet_amount != amount:
            raise ValueError("Le montant du pari est incorrect.")
        # Vérifiez si l'ID du match du pari est valide
        if not self.match_exists(bet_match_id):
            raise ValueError("L'ID du match du pari est incorrect.")
        # Vérifiez si le match a un gagnant déterminé
        if not self.match_has_winner(bet_match_id):
            raise ValueError("Le match n'a pas encore de gagnant déterminé.")
            # Vérifiez si le pari du joueur est gagnant
        if self.is_winning_bet(bet_match_id, bet_score):
            # Payez le pari
            # Écrivez votre code de paiement ici
            print(f"Le pari d'ID {bet_id} a été payé avec succès pour un montant de {amount}.")
        else:
            raise ValueError("Le pari n'est pas gagnant.")


    def user_exists(self,user_id: int) -> bool:

        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage avec l'ID donné
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False


    def bet_exists(self,bet_id: int) -> bool:

        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage avec l'ID donné
        cursor.execute("SELECT COUNT(*) FROM bets WHERE id=%s", (bet_id,))
        result = cursor.fetchall()

        if result:
            return True
        else:
            return False


    def match_exists(self,match_id: int) -> bool:
        conn = self.connection()
        cursor = conn.cursor()

        # Récupération des données du pariage avec l'ID donné
        cursor.execute("SELECT COUNT(*) matchs bets WHERE id=%s", (match_id,))
        result = cursor.fetchall()

        if result:
            return True
        else:
            return False

    def match_has_winner(self,match_id: int) -> bool:

        # Récupérez les informations du match
        match_info = Match().selectMatchById(match_id)
        home_score, away_score = match_info[2], match_info[3]

        # Si le score du match est connu, retournez True
        if home_score is not None and away_score is not None:
            return True
        else:
            # Si le score du match n'est pas connu, retournez False
            return False
