from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateEdit

from models.User import User
import uuid
import re
import datetime


class UserController:

    # Génération d'un UUID4
    unique_id = uuid.uuid4()

    # Conversion de l'UUID en entier
    unique_int = int(unique_id)

    # Limitation de l'entier à 4 chiffres
    code = unique_int % 10000

    balance = 0.00
    status = "ACTIVE"
    user_type = "USER"

    def update_account_info(self, last_name, first_name, username, date_of_birth, gender, nif_cin, phone, password,
                            confirmPassword, code=0):
        # Afficher un message d'erreur si un champ est vide
        if last_name == '' or first_name == '' or username == '' or date_of_birth == '' or gender == '' or phone == '' or nif_cin == '' or password == '' or confirmPassword == '':
            return "Tous les champs sont obligatoires"
        else:
            # Vérifier si le nom de famille est valide
            if self.validate_name(last_name):
                # Vérifier si le prénom est valide
                if self.validate_name(first_name):
                    # Vérifier si le numéro de téléphone est valide
                    if self.validate_phone(phone):
                        # Vérifier si le NIF est valide
                        if self.is_valid_nif(nif_cin):
                            # Vérifier si le nom d'utilisateur commence par une lettre
                            if self.starts_with_letter(username):
                                # Vérifier si le mot de passe et confirmPassword sont identiques
                                if password == confirmPassword:
                                    # Vérifier si le mot de passe a 8 caractères
                                    if self.has_8_characters(password):
                                        if self.is_major(date_of_birth):
                                            if not User().check_phone(phone):
                                                if not User().check_nif_cin(nif_cin):
                                                    if not User().check_username(username):
                                                        # Créer le compte avec les informations fournies
                                                        if code == 0:
                                                            print('add')
                                                            return User().add_account(self.code, last_name, first_name, username,
                                                                                         date_of_birth, gender, phone, nif_cin,
                                                                                         password, self.balance, self.status,
                                                                                         self.user_type)
                                                        else:
                                                            return User().update_account(last_name, first_name,
                                                                                         username,
                                                                                         date_of_birth, gender, phone,
                                                                                         nif_cin, code)
                                                    else:
                                                        return "Le nom d'utilisateur devrait etre unique."
                                                else:
                                                    return "Le nif ou cin devrait etre unique."
                                            else:
                                                return "Le numero de telephone devrait etre unique."
                                        else:
                                            return "L'utilisateur doit etre majeur pour s'inscrire."
                                    else:
                                        # Afficher un message d'erreur si le mot de passe n'a pas 8 caractères
                                        return "Le champs mot de passe doit contenir 8 caracteres."
                                else:
                                    # Afficher un message d'erreur si le mot de passe et confirmPassword ne sont pas identiques
                                    return  "Les mot de passe ne sont pas identiques."
                            else:
                                # Afficher un message d'erreur si le nom d'utilisateur ne commence pas par une lettre
                                return "Le champs nom d'utilisateur doit commencer par une lettre."
                        else:
                            # Afficher un message d'erreur si le NIF n'est pas valide
                            return f"Le NIF {nif_cin} n'est pas valide.\nUn nif contient neuf chiffres entiers."
                    else:
                        # Afficher un message d'erreur si le numéro de téléphone n'est pas au bon format
                        return "Le champ telephone doit respecter le format : +509 suivi de 8 chiffres sans espaces."
                else:
                    # Afficher un message d'erreur si le prénom n'est pas valide
                    return "Le champ prenom ne doit contenir que des chaines de caracteres et des espaces."

            else:
                # Afficher un message d'erreur si le nom de famille est n'est pas valide
                return "Le champ nom ne doit contenir que des chaines de caractères et des espaces."



    # def update_account_info(self, last_name, first_name, username, date_of_birth, gender, nif_cin, phone, id):
    #     # Afficher un message d'erreur si un champ est vide
    #     if last_name == '' or first_name == '' or username == '' or date_of_birth == '' or gender == '' or phone == '' or nif_cin == '':
    #         return "Tous les champs sont obligatoires"
    #     else:
    #         # Vérifier si le nom de famille est valide
    #         if self.validate_name(last_name):
    #             # Vérifier si le prénom est valide
    #             if self.validate_name(first_name):
    #                 # Vérifier si le numéro de téléphone est valide
    #                 if self.validate_phone(phone):
    #                     # Vérifier si le NIF est valide
    #                     if self.is_valid_nif(nif_cin):
    #                         # Vérifier si le nom d'utilisateur commence par une lettre
    #                         if self.starts_with_letter(username):
    #                             # Vérifier si le nom d'utilisateur a 18 ans ou plus
    #                             if self.is_major(date_of_birth):
    #                                 # Vérifier si le mot de passe et confirmPassword sont identiques
    #                                 return User().update_account(last_name, first_name, username,
    #                                                                          date_of_birth, gender, phone, nif_cin, id)
    #                             else:
    #                                 return 'Vous devez avoir plus de 18 ans pour vous connecter !'
    #                         else:
    #                             return "Le champ nom d'utilisateur ne doit contenir que des chaines de caracteres et des espaces"
    #                     else:
    #                         return f"Le NIF {nif_cin} n'est pas valide.\nUn nif contient neuf chiffres entiers."
    #                 else:
    #                     return "Le champ telephone doit respecter le format : +509 suivi de 8 chiffres"
    #             else:
    #                 return "Le champ prenom ne doit contenir que des chaines de caracteres et des espaces"
    #         else:
    #             return "Le champ nom ne doit contenir que des chaines de caractères et des espaces"



    def update_password(self, password, confirm_password, code):
        if password == confirm_password:
            # Vérifier si le mot de passe a 8 caractères
            if self.has_8_characters(password):
                # Mis a jour du compte avec les informations fournies
                return User().update_password(password, code)
            else:
                return "Le champs mot de passe doit contenir 8 caracteres"
        else:
            return "Les mot de passe ne sont pas identiques"




    def connect(self, username, password):
        if User().login(username, password) != 'inactive':
            # Récupération des données de l'utilisateur
            # user_data = User().login(username, password)
            if User().login(username, password) != 'delete':
                if User().login(username, password) == 'valid':
                    return "valid"
                else:
                    return "Nom d'utilisateur ou mot de passe incorrect."
            else:
                return "Ce compte a ete supprime.\nVeuillez creer un autre."
        else:
            return "Ce compte est inactif.\nDemandez a l'administateur de le rendre actif."

    def validate_name(self, value):
        if isinstance(value, str):
            return bool(re.match(r"^[a-zA-Z ]+$", value))
        return False

    def validate_phone(self, value):
        pattern = r'^\+509\d{8}$'

        if re.search(pattern, value):
            return True
        else:
            return False

    def is_major(self,date_naissance):
        aujourdhui = datetime.date.today()
        age = aujourdhui.year - date_naissance.year
        if age >= 18:
            return True
        elif age == 18:
            if date_naissance.month > aujourdhui.month:
                return False
            elif date_naissance.month == aujourdhui.month:
                if date_naissance.day > aujourdhui.day:
                    return False
            return True

    def is_valid_nif(self, nif: str) -> bool:
        if not nif or len(nif) != 9:
            return False
        return nif.isdigit()

    def starts_with_letter(self, string):
        return string[0].isalpha()

    def has_8_characters(self, string):
        return bool(re.match(r"^.{8}$", string))

    def user_auth(self):
        return User().display_UserAuth()

    def disconnect(self):
        User().truncate_userAuth()

