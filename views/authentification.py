import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, \
    QLineEdit, QRadioButton, QDateEdit, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap
from controllers.UserController import UserController
from models.DBConnection import DBConnection
from models.User import User
import sys


class LoginDialog(QDialog):
    def __init__(self, parent):
        super(LoginDialog, self).__init__(parent)
        self.parent = parent
        self.setFixedSize(500, 500)
        self.setWindowTitle(" Connection | GeeBet")
        self.center()
        self.setStyleSheet(open('../assets/css/style.css', "r").read())
        # Création du layout vertical principal
        self.mainLayout = QVBoxLayout()
        if DBConnection().connection():
            if not User().display_UserAuth():
                self.initUI()
            else:
                self.connect()

    def initUI(self):
        self.groupBox = QGroupBox()
        self.groupBox.setFixedSize(450, 450)
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()


        # Creation d'un QLabel pour l'image
        self.lbl_img = QLabel()

        self.img = QPixmap("../assets/LogoBetGee.png")

        smaller  = self.img.scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)

        self.lbl_img.setPixmap(smaller)
        self.lbl_img.setAlignment(Qt.AlignCenter)


        self.verticalLayout.addWidget(self.lbl_img)

        self.title = QLabel("Informations de connection")
        self.title.setAlignment(Qt.AlignCenter)
        self.usernameLabel = QLabel("Nom d'utilisateur")
        self.usernameField = QLineEdit()
        self.usernameField.setPlaceholderText("Saisir Username")
        self.usernameField.setObjectName("fields")

        self.passwordLabel = QLabel("Mot de passe")
        self.passwordField = QLineEdit()
        self.passwordField.setEchoMode(QLineEdit.Password)
        self.passwordField.setPlaceholderText("Saisir votre mot de passe")
        self.passwordField.setObjectName("fields")
        self.loginButton = QPushButton('Se connecter', self)
        self.loginButton.setObjectName("btn_primary")
        self.account_exist = QLabel("Vous n'avez pas encore de compte ?")
        self.registerButton = QPushButton("S'inscrire", self)
        self.registerButton.setObjectName("btn")


        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addWidget(self.usernameLabel)
        self.verticalLayout.addWidget(self.usernameField)
        self.verticalLayout.addWidget(self.passwordLabel)
        self.verticalLayout.addWidget(self.passwordField)
        self.verticalLayout.addWidget(self.loginButton)

        self.horizontalLayout.addWidget(self.account_exist)
        self.horizontalLayout.addWidget(self.registerButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)

        self.loginButton.clicked.connect(self.connexion)
        self.registerButton.clicked.connect(self.showRegister)

        self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)
        self.mainLayout.setStretch(500, 500)
        self.setLayout(self.mainLayout)

        self.groupBox.setAlignment(Qt.AlignCenter)
        self.show()

    # Ajout de cette méthode pour ferme la fenêtre de login et ouvrir  la fenêtre de register
    def showRegister(self):
        self.close()
        registerDialog = RegisterDialog(self.parent)
        registerDialog.exec_()

    # Ajout de cette méthode pour ferme la fenêtre de register et ouvrir  la fenêtre de login
    def showLogin(self):
        self.close()
        loginDialog = LoginDialog(self.parent)
        loginDialog.exec_()


    # Ajout de cette méthode pour connecter l'utilisateur au menu principal
    def connect(self):
        self.parent.show()
        self.close()

    def restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # Ajout de cette méthode pour centrer la fenêtre
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def connexion(self):
        response = UserController().connect(self.usernameField.text(), self.passwordField.text())
        if response == "valid":
            self.restart()
        else:
            QMessageBox.about(self, 'Erreur', response)


class RegisterDialog(QDialog):
    def __init__(self, parent):
        super(RegisterDialog, self).__init__(parent)
        self.setFixedSize(950, 670)
        self.setWindowTitle(" Inscription | GeeBet")
        self.center()
        self.mainLayout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        # Création des QGroupBox
        group_box_1 = QGroupBox()
        group_box_2 = QGroupBox("Informations du compte")

        # Création du layout horizontal
        h_layout = QHBoxLayout()

        # Groupe Box 2

        # Champ Nom
        self.lastNameLabel = QLabel('Nom')
        self.lastNameField = QLineEdit()
        self.lastNameField.setPlaceholderText("Saisir votre nom")
        self.lastNameField.setObjectName("fields")
        self.lastNameField.setTextMargins(3, 0, 3, 0)
        self.lastNameField.setMinimumWidth(200)
        self.lastNameField.setMaximumWidth(300)

        # Champ prenom
        self.firstNameLabel = QLabel('Prenom')
        self.firstNameField = QLineEdit()
        self.firstNameField.setPlaceholderText("Saisir votre prenom")
        self.firstNameField.setObjectName("fields")
        self.firstNameField.setTextMargins(3, 0, 3, 0)
        self.firstNameField.setMinimumWidth(200)
        self.firstNameField.setMaximumWidth(300)

        # Champ Nom d'utilisateur
        self.userNameLabel = QLabel("Nom d'utilisateur")
        self.userNameField = QLineEdit()
        self.userNameField.setPlaceholderText("Saisir votre nom d'utilisateur")
        self.userNameField.setObjectName("fields")
        self.userNameField.setTextMargins(3, 0, 3, 0)
        self.userNameField.setMinimumWidth(200)
        self.userNameField.setMaximumWidth(300)

        # Champ sexe
        self.genderLabel = QLabel('Sexe')
        self.genderLabel.setContentsMargins(3, 0, 0, 0)
        self.radioButton1 = QRadioButton("M")
        self.radioButton2 = QRadioButton("F")
        self.radioButton1.setChecked(True)
        self.horizontalLayout = QHBoxLayout()
        self.genderGroup = QGroupBox()

        # Ajout des composants dans le layout horizontal
        self.horizontalLayout.addWidget(self.radioButton1)
        self.horizontalLayout.addWidget(self.radioButton2)

        # Ajout des composants dans le GroupBox
        self.genderGroup.setLayout(self.horizontalLayout)
        self.genderGroup.setContentsMargins(30, 0, 3, 0)
        self.genderGroup.setMinimumWidth(200)
        self.genderGroup.setMaximumWidth(300)

        # Champ date de naissance
        self.dateOfBirthLabel = QLabel('Date de naissance')
        self.dateOfBirthField = QDateEdit()

        # current_date = QDate.currentDate()

        # Affichez la date courante dans le champ de date
        # self.dateOfBirthField.setDate(current_date)
        self.dateOfBirthField.setDisplayFormat("dd/MM/yyyy")
        self.dateOfBirthField.setObjectName("fields")
        self.dateOfBirthField.setCalendarPopup(True)
        self.dateOfBirthField.setContentsMargins(3, 0, 3, 0)
        self.dateOfBirthField.setMinimumWidth(200)
        self.dateOfBirthField.setMaximumWidth(300)

        # Champ téléphone
        self.phoneLabel = QLabel('Telephone')
        self.phoneField = QLineEdit()
        self.phoneField.setPlaceholderText("+(509) 3698-8433")
        self.phoneField.setObjectName("fields")
        self.phoneField.setTextMargins(3, 0, 3, 0)
        self.phoneField.setMinimumWidth(200)
        self.phoneField.setMaximumWidth(300)

        # Champ NIF/CIN
        self.nif_cinLabel = QLabel('NIF/CIN')
        self.nif_cinField = QLineEdit()
        self.nif_cinField.setPlaceholderText("Saisir votre nif ou votre cin")
        self.nif_cinField.setObjectName("fields")
        self.nif_cinField.setTextMargins(3, 0, 3, 0)
        self.nif_cinField.setMinimumWidth(200)
        self.nif_cinField.setMaximumWidth(300)

        # Champ mot de passe
        self.passwordLabel = QLabel('Mot de passe')
        self.passwordField = QLineEdit()
        self.passwordField.setPlaceholderText("Saisir un mot de passe")
        self.passwordField.setObjectName("fields")
        self.passwordField.setTextMargins(3, 0, 3, 0)
        self.passwordField.setMinimumWidth(200)
        self.passwordField.setMaximumWidth(300)
        self.passwordField.setEchoMode(QLineEdit.Password)

        # Champ confirmation de mot de passe
        self.confirmPasswordLabel = QLabel('Confirmation de mot de passe')
        self.confirmPasswordField = QLineEdit()
        self.confirmPasswordField.setObjectName("fields")
        self.confirmPasswordField.setPlaceholderText("Confirmer votre mot de passe")
        self.confirmPasswordField.setTextMargins(3, 0, 3, 0)
        self.confirmPasswordField.setMinimumWidth(200)
        self.confirmPasswordField.setMaximumWidth(300)
        self.confirmPasswordField.setEchoMode(QLineEdit.Password)

        # Ajout des colonnes dans le add formlayout

        # Groupe Box 1

        # Creation d'un QLabel pour l'image
        self.lbl_img = QLabel()

        self.img = QPixmap("../assets/messi.jpg")

        self.lbl_img.setPixmap(self.img)
        self.lbl_img.setAlignment(Qt.AlignCenter)
        self.lbl_img.setStyleSheet("border-radius: 50px; ")

        self.Vbox_img = QVBoxLayout()
        self.Vbox_img.addWidget(self.lbl_img)
        group_box_1.setLayout(self.Vbox_img)


        self.Vbox = QVBoxLayout()
        self.Hbox = QVBoxLayout()
        self.Vbox.addWidget(self.lastNameLabel)
        self.Vbox.addWidget(self.lastNameField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.firstNameLabel)
        self.Vbox.addWidget(self.firstNameField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.userNameLabel)
        self.Vbox.addWidget(self.userNameField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.dateOfBirthLabel)
        self.Vbox.addWidget(self.dateOfBirthField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.genderLabel)
        self.Vbox.addWidget(self.genderGroup)
        self.verticalLayout.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.nif_cinLabel)
        self.Vbox.addWidget(self.nif_cinField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.phoneLabel)
        self.Vbox.addWidget(self.phoneField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.passwordLabel)
        self.Vbox.addWidget(self.passwordField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.confirmPasswordLabel)
        self.Vbox.addWidget(self.confirmPasswordField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.loginButton = QPushButton("Se connecter", self)
        self.loginButton.setObjectName("btn")
        self.account_exist = QLabel("Vous avez deja un compte ?")
        self.registerButton = QPushButton("S'inscrire", self)
        self.registerButton.setObjectName("btn_primary")

        self.horizontalLayout = QHBoxLayout()

        self.verticalLayout.addWidget(self.registerButton)

        self.horizontalLayout.addWidget(self.account_exist)
        self.horizontalLayout.addWidget(self.loginButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        group_box_2.setLayout(self.verticalLayout)
        group_box_2.setAlignment(Qt.AlignCenter)

        # Ajout des QGroupBox au layout horizontal
        h_layout.addWidget(group_box_1)
        h_layout.addWidget(group_box_2)



        self.registerButton.clicked.connect(self.registration)
        self.loginButton.clicked.connect(self.showLogin)
        self.show()

        self.mainLayout.setAlignment(Qt.AlignCenter)

        # Ajout du layout horizontal au layout vertical principal
        self.setLayout(h_layout)

    # Ajout de cette méthode pour ferme la fenêtre de register et ouvrir  la fenêtre de login
    def showLogin(self):
        self.close()
        loginDialog = LoginDialog(self.parent())
        loginDialog.exec_()

    # Ajout de cette méthode pour ferme la fenêtre de login et ouvrir  la fenêtre de register
    def showRegister(self):
        self.close()
        registerDialog = RegisterDialog(self.parent())
        registerDialog.exec_()

    # Ajout de cette méthode pour centrer la fenêtre
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def registration(self):
        gender = None

        if self.radioButton1.isChecked():
            gender = self.radioButton1.text()
        else:
            gender = self.radioButton2.text()

        response = UserController().update_account_info(
            self.lastNameField.text(),
            self.firstNameField.text(),
            self.userNameField.text(),
            self.dateOfBirthField.date().toPyDate(),
            gender,
            self.nif_cinField.text(),
            self.phoneField.text(),
            self.passwordField.text(),
            self.confirmPasswordField.text()
        )
        if response == "add_success":
            self.showLogin()
        else:
            QMessageBox.about(self, 'Erreur', response)



