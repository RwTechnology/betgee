import re
from models.Retrait import Retrait
from models.User import User


class RetraitAccountController:

    def add_retrait(self, code, amount, date):
        # Afficher un message d'erreur si un champ est vide
        if amount == '' or code == '':
            return "Veuillez renseigner tous les champs !"
        else:
            if User().select_userById(code):
                if User().select_userById(code)[11] != "admin":
                    if self.check_float(amount):
                        if float(User().select_userById(code)[9]) > float(amount):
                            return Retrait().insert(code, amount, date)
                        else:
                            return "Vous n'avez pas assez d'argent !"
                    else:
                        return 'Veuillez saisir un nombre reel ou entier'
                else:
                    return "Ce compte n'est pas eligible"
            else:
                return 'Ce code est incorrect'



    def check_float(self, input_str):
        try:
            float(input_str)
            return True
        except ValueError:
            return False

