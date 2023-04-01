from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QGroupBox, QTimeEdit, \
    QDateEdit, QDialog, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QSize,QDate
from models.Match import Match
from controllers.MatchController import MatchController
import uuid


class AddMatch(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet(open("../assets/css/style.css", "r").read())
        self.setFixedSize(950, 750)
        self.setWindowTitle(" Ajout de match | GeeBet")
        self.center()
        self.mainLayout = QVBoxLayout()

        # Création des QGroupBox
        group_box_1 = QGroupBox()
        group_box_2 = QGroupBox("Informations du match")

        # Création du layout horizontal
        h_layout = QHBoxLayout()

        # Groupe Box 2
        # Champ type match
        self.typeMatchLabel = QLabel('Type Match')
        type = ["Championnat", "Coupe du monde", "Eliminatoire", "Amical"]
        self.typeMatch = QComboBox()

        self.typeMatch.setObjectName("fields")
        self.typeMatch.setStyleSheet(self.styleSheet())

        self.typeMatch.addItems(type)
        self.typeMatch.setContentsMargins(3, 0, 3, 0)
        self.typeMatch.setMinimumWidth(200)
        self.typeMatch.setMaximumWidth(300)

        # Champ pays
        self.countryLabel = QLabel('Pays')
        country = ["Espagne", "Allemagne", "Angleterre", "Italie", "Brezil", "Argentine"]
        self.countryField = QComboBox()

        self.countryField.setObjectName("fields")
        self.countryField.setStyleSheet(self.styleSheet())

        self.countryField.addItems(country)
        self.countryField.setContentsMargins(3, 0, 3, 0)
        self.countryField.setMinimumWidth(200)
        self.countryField.setMaximumWidth(300)

        # Champ heure match
        self.matchTimeLabel = QLabel("Heure match")
        self.matchTimeField = QTimeEdit()

        self.matchTimeField.setObjectName("fields")
        self.matchTimeField.setStyleSheet(self.styleSheet())

        self.matchTimeField.setContentsMargins(3, 0, 3, 0)
        self.matchTimeField.setMinimumWidth(200)
        self.matchTimeField.setMaximumWidth(300)

        # Champ equipe receveuse
        self.matchTeam1Label = QLabel("Equipe receveuse")
        self.matchTeam1Field = QLineEdit()
        self.matchTeam1Field.setObjectName("fields")
        self.matchTeam1Field.setStyleSheet(self.styleSheet())

        self.matchTeam1Field.setPlaceholderText("Saisir le nom de l'equipe receveuse")
        self.matchTeam1Field.setTextMargins(3, 0, 3, 0)
        self.matchTeam1Field.setMinimumWidth(200)
        self.matchTeam1Field.setMaximumWidth(300)

        self.horizontalLayout = QHBoxLayout()

        # Champ date match
        self.matchDateLabel = QLabel('Date match')
        self.matchDateField = QDateEdit()
        self.matchDateField.setObjectName("fields")
        self.matchDateField.setStyleSheet(self.styleSheet())

        current_date = QDate.currentDate()

        # Affichez la date courante dans le champ de date
        self.matchDateField.setDate(current_date)
        self.matchDateField.setDisplayFormat("dd/MM/yyyy")
        self.matchDateField.setCalendarPopup(True)
        self.matchDateField.setContentsMargins(3, 0, 3, 0)
        self.matchDateField.setMinimumWidth(200)
        self.matchDateField.setMaximumWidth(300)

        # Champ equipe visiteuse
        self.matchTeam2Label = QLabel('Equipe receveuse')
        self.matchTeam2Field = QLineEdit()
        self.matchTeam2Field.setObjectName("fields")
        self.matchTeam2Field.setStyleSheet(self.styleSheet())

        self.matchTeam2Field.setPlaceholderText("Saisir le nom de l'equipe visiteuse")
        self.matchTeam2Field.setTextMargins(3, 0, 3, 0)
        self.matchTeam2Field.setMinimumWidth(200)
        self.matchTeam2Field.setMaximumWidth(300)

        # Champ Cote
        self.matchCoteLabel = QLabel('Cote')
        self.matchCoteField = QLineEdit()
        self.matchCoteField.setObjectName("fields")
        self.matchCoteField.setStyleSheet(self.styleSheet())

        self.matchCoteField.setPlaceholderText("Saisir le cote du match : format: 1.2")
        self.matchCoteField.setTextMargins(3, 0, 3, 0)
        self.matchCoteField.setMinimumWidth(200)
        self.matchCoteField.setMaximumWidth(300)

        # Champ score match
        self.matchScoreLabel = QLabel('Score du match')
        self.matchScoreField = QLineEdit()
        self.matchScoreField.setObjectName("fields")
        self.matchScoreField.setStyleSheet(self.styleSheet())

        # self.matchScoreField.setText('0:0')
        self.matchScoreField.setPlaceholderText("Saisir le score du match : format: 1:0")
        self.matchScoreField.setContentsMargins(3, 0, 3, 0)
        self.matchScoreField.setMinimumWidth(200)
        self.matchScoreField.setMaximumWidth(300)

        # Champ etat match
        self.matchStateLabel = QLabel('Etat du match')
        self.matchStateTab = ["N", "E", "T", "A", "S"]
        self.matchStateField = QComboBox()
        self.matchStateField.setObjectName("fields")
        self.matchStateField.setStyleSheet(self.styleSheet())
        self.matchStateField.addItems(self.matchStateTab)
        self.matchStateField.setContentsMargins(3, 0, 3, 0)
        self.matchStateField.setMinimumWidth(200)
        self.matchStateField.setMaximumWidth(300)

        # Ajout des colonnes dans le add formlayout

        # Groupe Box 1

        # Creation d'un QLabel pour l'image
        self.lbl_img = QLabel()

        self.img = QPixmap("../assets/messi_10.jpg")

        self.lbl_img.setPixmap(self.img)
        self.lbl_img.setAlignment(Qt.AlignCenter)
        self.lbl_img.setStyleSheet("border-radius: 50px; ")

        self.Vbox_img = QVBoxLayout()
        self.Vbox_img.addWidget(self.lbl_img)
        group_box_1.setLayout(self.Vbox_img)

        # Ajout des colonnes dans le add formlayout
        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.typeMatchLabel)
        self.Vbox.addWidget(self.typeMatch)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.countryLabel)
        self.Vbox.addWidget(self.countryField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.matchDateLabel)
        self.Vbox.addWidget(self.matchDateField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchTimeLabel)
        self.Vbox.addWidget(self.matchTimeField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.matchTeam1Label)
        self.Vbox.addWidget(self.matchTeam1Field)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchTeam2Label)
        self.Vbox.addWidget(self.matchTeam2Field)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.matchCoteLabel)
        self.Vbox.addWidget(self.matchCoteField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchStateLabel)
        self.Vbox.addWidget(self.matchStateField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchScoreLabel)
        self.Vbox.addWidget(self.matchScoreField)

        self.verticalLayout.addLayout(self.Vbox)


        self.verticalLayout.setAlignment(Qt.AlignCenter)

        self.save_match_info_button = QPushButton("Ajouter", self)
        self.save_match_info_button.setObjectName("btn_primary")
        self.save_match_info_button.setStyleSheet(self.styleSheet())



        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.save_match_info_button)


        self.groupBox = QGroupBox()
        self.groupBox.setLayout(self.verticalLayout)
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.show()
        self.mainLayout.addWidget(self.groupBox)

        self.mainLayout.setAlignment(Qt.AlignCenter)

        group_box_2.setLayout(self.verticalLayout)
        group_box_2.setAlignment(Qt.AlignCenter)

        # Ajout des QGroupBox au layout horizontal
        h_layout.addWidget(group_box_1)
        h_layout.addWidget(group_box_2)

        self.show()

        self.mainLayout.setAlignment(Qt.AlignCenter)

        # Ajout du layout horizontal au layout vertical principal
        self.setLayout(h_layout)

        self.setLayout(self.mainLayout)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Les evenements
        self.save_match_info_button.clicked.connect(self.registration)


    def registration(self):
        # Génération d'un UUID4
        unique_id = uuid.uuid4()

        # Conversion de l'UUID en entier
        unique_int = int(unique_id)

        # Limitation de l'entier à 4 chiffres
        code = unique_int % 10000
        print("coyt",self.matchCoteField.text())

        response = MatchController().add_account_info(
                code,
                self.typeMatch.currentText(),
                self.countryField.currentText(),
                self.matchDateField.date().toPyDate(),
                self.matchTimeField.text(),
                self.matchTeam1Field.text(),
                self.matchTeam2Field.text(),
                self.matchCoteField.text(),
                self.matchScoreField.text(),
                self.matchStateField.currentText()
            )
        if response == 'add_success':
            QMessageBox.about(self, 'Informations', "Insertion effectuee")
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

