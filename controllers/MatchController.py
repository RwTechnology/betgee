import re

from models.Match import Match
import uuid


class MatchController:

    def add_account_info(self, code, match_type, country, match_date, match_time, receiver_team, visitor_team, cote_match, score, state):
        # Afficher un message d'erreur si un champ est vide

        print(code,match_type,country,match_date,match_time,receiver_team,visitor_team,cote_match,score,state)

        if match_type == '' or country == '' or match_date == '' or match_time == '' or receiver_team == '' or visitor_team == '' or cote_match == '' or score == '' or state == '':
            return "Tous les champs sont obligatoires"
        else:
            if f'{receiver_team}'.lower() == f'{visitor_team}'.lower():
                return "Les deux equipes doivent etre differentes"
            else:
                if not self.is_valid_score(score):
                    return "Vous devez respecter le format 1:0"
                try:
                    Match().insert(code, match_type, country, match_date, match_time, receiver_team, visitor_team,cote_match, score, state)
                except Exception as e:
                    return "Error adding match: {}".format(str(e))
                return 'add_success'

    # Fonction de validation du format 3:3
    def is_valid_score(self,score):
        # Vérifie si le score est au format attendu (nombre:nombre)
        return bool(re.match(r'^\d+:\d+$', str(score)))



    def update_account_info(self, match_type, country, match_date, match_time, receiver_team, visitor_team, cote_match, score, state, code):
        # Afficher un message d'erreur si un champ est vide
        if match_type == '' or country == '' or match_date == '' or match_time == '' or receiver_team == '' or visitor_team == '' or cote_match == '' or score == '' or state == '':
            return "Tous les champs sont obligatoires"
        else:
            if self.is_valid_score(score):
                # Modifier le match avec les informations fournies
                Match().update(match_type, country, match_date, match_time, receiver_team, visitor_team, cote_match, score, state, code)
                return 'update_success'
            else:
                return "Veuillez respecter le format de score ,score1:score2"

    def displayMatch(self):
        return Match().selectMatchInfo()

    # Fonction de validation du format 3:3
    def is_valid_score(self,score):
        # Vérifie si le score est au format attendu (nombre:nombre)
        return bool(re.match(r'^\d+:\d+$', str(score)))
