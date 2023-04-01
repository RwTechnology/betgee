import re
from models.RechargeAccount import RechargeAccount
from models.User import User


class RechargeAccountController:

    def add_credit(self, code, amount, credit_date):
        # Afficher un message d'erreur si un champ est vide
        if amount == '' or code == '':
            return "Veuillez renseigner tous les champs !"
        else:
            if User().select_userById(code) :
                if User().select_userById(code)[11] != "admin":
                    if self.check_float(amount):
                        print(float(amount))
                        if float(amount)>=75000.0:
                            return 'le montant doit etre inferieur a 75000'
                        else:
                            return RechargeAccount().insert(code, amount, credit_date)
                    else:
                        return 'Veuillez saisir un nombre reel ou entier'
                else:
                    return "Ce compte n'est pas eligible pour recharger"
            else:
                return 'Ce code est incorrect'



    def check_float(self, input_str):
        try:
            float(input_str)
            return True
        except ValueError:
            return False

