from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QDialog, QRadioButton, QLineEdit, QDateEdit, \
    QGroupBox, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QSize,QDate
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from models.Match import Match
from controllers.UserController import UserController
from models.User import User


class PasswordDialog(QDialog):

    def __init__(self, parent, compte_id):
        super().__init__(parent)
        self.setFixedSize(350, 350)
        self.setWindowTitle(" Mise a jour de mot de passe | GeeBet")
        self.center()
        self.mainLayout = QVBoxLayout()

        self.code = compte_id

        # Création des QGroupBox
        group_box_1 = QGroupBox()
        group_box_2 = QGroupBox("Informations du compte")

        # Création du layout horizontal
        self.groupBox = QGroupBox()
        self.groupBox.setFixedSize(300, 300)
        self.groupBox.setObjectName("grpbx")

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()

        # Groupe Box 2

        self.passwordLabel = QLabel('Mot de passe')
        self.passwordField = QLineEdit()
        self.passwordField.setPlaceholderText("Saisir un mot de passe")
        self.passwordField.setTextMargins(3, 0, 3, 0)
        self.passwordField.setMinimumWidth(200)
        self.passwordField.setMaximumWidth(300)
        self.passwordField.setEchoMode(QLineEdit.Password)

        # Champ confirmation de mot de passe
        self.confirmPasswordLabel = QLabel('Confirmation de mot de passe')
        self.confirmPasswordField = QLineEdit()
        self.confirmPasswordField.setPlaceholderText("Confirmer votre mot de passe")
        self.confirmPasswordField.setTextMargins(3, 0, 3, 0)
        self.confirmPasswordField.setMinimumWidth(200)
        self.confirmPasswordField.setMaximumWidth(300)
        self.confirmPasswordField.setEchoMode(QLineEdit.Password)

        # Ajout des colonnes dans le add formlayout
        self.verticalLayout = QVBoxLayout()

        self.Vbox.addWidget(self.passwordLabel)
        self.Vbox.addWidget(self.passwordField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)
        self.verticalLayout.setAlignment(Qt.AlignCenter)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()

        self.Vbox.addWidget(self.confirmPasswordLabel)
        self.Vbox.addWidget(self.confirmPasswordField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)
        self.verticalLayout.setAlignment(Qt.AlignCenter)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()

        self.update_user_info_button = QPushButton("Modifier", self)
        self.update_user_info_button.setStyleSheet(
            "background-color: #38BDF9;"
            "padding: 10px;"
            "border-radius: 5px;"
        )

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.update_user_info_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox.setLayout(self.verticalLayout)

        self.show()
        self.mainLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)

        self.setLayout(self.mainLayout)
        self.setStyleSheet(
            "padding: 10px;"
        )

        # Les evenements
        self.update_user_info_button.clicked.connect(self.change_password)

    def change_password(self):

        response = UserController().update_password(
            self.passwordField,
            self.confirmPasswordField,
            self.code
        )
        if response == "update_success":
            QMessageBox.about(self, 'Informations', "Mot de passe  mis a jour a jour !")
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