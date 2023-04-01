from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QDialog, QRadioButton, QLineEdit, QDateEdit, \
    QGroupBox, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QSize,QDate
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from models.Match import Match
from controllers.UserController import UserController
from models.User import User


class CompteDialog(QDialog):

    def __init__(self, parent, compte_id,first_name,last_name,username,date_of_birth,gender,phone,nif_cin,password,balance,status,user_type):
        super().__init__(parent)
        self.setFixedSize(950, 670)
        self.setWindowTitle(" Mise a jour de compte | GeeBet")
        self.center()
        self.mainLayout = QVBoxLayout()

        self.code = compte_id
        # Création des QGroupBox
        group_box_1 = QGroupBox()
        group_box_2 = QGroupBox("Informations du compte")

        # Création du layout horizontal
        h_layout = QHBoxLayout()

        # Groupe Box 2

        # Champ Nom
        self.lastNameLabel = QLabel('Nom')
        self.lastNameField = QLineEdit(last_name)
        self.lastNameField.setPlaceholderText("Saisir votre nom")
        self.lastNameField.setObjectName("fields")
        self.lastNameField.setTextMargins(3, 0, 3, 0)
        self.lastNameField.setMinimumWidth(200)
        self.lastNameField.setMaximumWidth(300)

        # Champ prenom
        self.firstNameLabel = QLabel('Prenom')
        self.firstNameField = QLineEdit(first_name)
        self.firstNameField.setPlaceholderText("Saisir votre prenom")
        self.firstNameField.setObjectName("fields")
        self.firstNameField.setTextMargins(3, 0, 3, 0)
        self.firstNameField.setMinimumWidth(200)
        self.firstNameField.setMaximumWidth(300)

        # Champ Nom d'utilisateur
        self.userNameLabel = QLabel("Nom d'utilisateur")
        self.userNameField = QLineEdit(username)
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

        if gender == 'M':
            self.radioButton1.setChecked(True)
        elif gender == 'F':
            self.radioButton2.setChecked(True)
        else:
            self.radioButton1.setChecked(None)

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

        date_str = date_of_birth
        # Créer un objet QDate à partir de la chaîne de caractères
        date = QDate.fromString(date_str, "yyyy-MM-dd")


        # Affichez la date courante dans le champ de date
        self.dateOfBirthField.setDate(date)
        # self.dateOfBirthField.setDisplayFormat("dd/MM/yyyy")
        self.dateOfBirthField.setObjectName("fields")
        self.dateOfBirthField.setCalendarPopup(True)
        self.dateOfBirthField.setContentsMargins(3, 0, 3, 0)
        self.dateOfBirthField.setMinimumWidth(200)
        self.dateOfBirthField.setMaximumWidth(300)

        # Champ téléphone
        self.phoneLabel = QLabel('Telephone')
        self.phoneField = QLineEdit(phone)
        self.phoneField.setPlaceholderText("+(509) 3698-8433")
        self.phoneField.setObjectName("fields")
        self.phoneField.setTextMargins(3, 0, 3, 0)
        self.phoneField.setMinimumWidth(200)
        self.phoneField.setMaximumWidth(300)

        # Champ NIF/CIN
        self.nif_cinLabel = QLabel('NIF/CIN')
        self.nif_cinField = QLineEdit(nif_cin)
        self.nif_cinField.setPlaceholderText("Saisir votre nif ou votre cin")
        self.nif_cinField.setObjectName("fields")
        self.nif_cinField.setTextMargins(3, 0, 3, 0)
        self.nif_cinField.setMinimumWidth(200)
        self.nif_cinField.setMaximumWidth(300)

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


        self.update_user_info_button = QPushButton("Modifier", self)
        self.update_user_info_button.setObjectName("btn_primary")

        self.horizontalLayout = QHBoxLayout()

        self.verticalLayout.addWidget(self.update_user_info_button)
        group_box_2.setLayout(self.verticalLayout)
        group_box_2.setAlignment(Qt.AlignCenter)

        # Ajout des QGroupBox au layout horizontal
        h_layout.addWidget(group_box_1)
        h_layout.addWidget(group_box_2)

        self.update_user_info_button.clicked.connect(self.update)
        self.show()

        self.mainLayout.setAlignment(Qt.AlignCenter)

        # Ajout du layout horizontal au layout vertical principal
        self.setLayout(h_layout)


    def update(self):
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
                self.code
            )
            if response == "update_success":
                QMessageBox.about(self, 'Informations', "Compte  mis a jour a jour !")
                self.close()
            else:
                QMessageBox.about(self, 'Erreur', response)

    # Ajout de cette méthode pour centrer la fenêtre
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())