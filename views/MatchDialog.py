from PyQt5 import QtPrintSupport
from PyQt5.QtGui import QPixmap, QTextImageFormat, QTextCursor, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QGroupBox, QTimeEdit, \
    QDateEdit, QDialog, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QSize, QDate, QUrl, QTime
from models.Match import Match
from controllers.MatchController import MatchController
from models.User import User


class MatchDialog(QDialog):

    def __init__(self, parent, match_id, typeMatch, country, matchDate, matchTime, matchTeam1, matchTeam2, matchCote, matchScore, matchState):
        super().__init__(parent)
        self.match_id = match_id
        self.setStyleSheet(open("../assets/css/style.css", "r").read())
        self.setFixedSize(950, 670)
        self.setWindowTitle(" Mise a jour de match | GeeBet")
        self.center()
        self.mainLayout = QVBoxLayout()

        self.code = match_id
        match_keys = ["Id", "Type Match", "Pays", "Date Match", "Heure Match", "Equipe Receveuse", "Equipe Visiteuse", "Cote","Score", "Etat"]
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
        self.typeMatch.setCurrentText(typeMatch)
        self.typeMatch.setContentsMargins(3, 0, 3, 0)
        self.typeMatch.setMinimumWidth(200)
        self.typeMatch.setMaximumWidth(300)

        # Champ pays
        self.countryLabel = QLabel('Pays')
        country = ["Espagne", "Allemagne", "Angleterre", "Italie", "Bresil", "Argentine"]
        self.countryField = QComboBox()

        self.countryField.setObjectName("fields")
        self.countryField.setStyleSheet(self.styleSheet())

        self.countryField.addItems(country)
        self.countryField.setContentsMargins(3, 0, 3, 0)
        self.countryField.setMinimumWidth(200)
        self.countryField.setMaximumWidth(300)

        # Champ heure match

        # Créer un objet QDate à partir de la chaîne de caractères
        time_edit = QTime().fromString(matchTime)

        self.matchTimeLabel = QLabel("Heure match")
        self.matchTimeField = QTimeEdit()

        self.matchTimeField.setTime(time_edit)

        self.matchTimeField.setObjectName("fields")
        self.matchTimeField.setStyleSheet(self.styleSheet())

        self.matchTimeField.setContentsMargins(3, 0, 3, 0)
        self.matchTimeField.setMinimumWidth(200)
        self.matchTimeField.setMaximumWidth(300)

        # Champ equipe receveuse
        self.matchTeam1Label = QLabel("Equipe receveuse")
        self.matchTeam1Field = QLineEdit(matchTeam1)
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

        date_str = matchDate
        # Créer un objet QDate à partir de la chaîne de caractères
        date = QDate.fromString(date_str, "yyyy-MM-dd")

        # Affichez la date courante dans le champ de date
        self.matchDateField.setDate(date)
        self.matchDateField.setDisplayFormat("dd/MM/yyyy")
        self.matchDateField.setCalendarPopup(True)
        self.matchDateField.setContentsMargins(3, 0, 3, 0)
        self.matchDateField.setMinimumWidth(200)
        self.matchDateField.setMaximumWidth(300)

        # Champ equipe visiteuse
        self.matchTeam2Label = QLabel('Equipe visiteuse')
        self.matchTeam2Field = QLineEdit(matchTeam2)
        self.matchTeam2Field.setObjectName("fields")
        self.matchTeam2Field.setStyleSheet(self.styleSheet())

        self.matchTeam2Field.setPlaceholderText("Saisir le nom de l'equipe visiteuse")
        self.matchTeam2Field.setTextMargins(3, 0, 3, 0)
        self.matchTeam2Field.setMinimumWidth(200)
        self.matchTeam2Field.setMaximumWidth(300)

        # Champ Cote
        self.matchCoteLabel = QLabel('Cote')
        self.matchCoteField = QLineEdit(matchCote)
        self.matchCoteField.setObjectName("fields")
        self.matchCoteField.setStyleSheet(self.styleSheet())

        self.matchCoteField.setPlaceholderText("Saisir le cote du match")
        self.matchCoteField.setTextMargins(3, 0, 3, 0)
        self.matchCoteField.setMinimumWidth(200)
        self.matchCoteField.setMaximumWidth(300)

        # Champ score match
        self.matchScoreLabel = QLabel('Score du match')
        self.matchScoreField = QLineEdit(matchScore)
        self.matchScoreField.setObjectName("fields")
        self.matchScoreField.setStyleSheet(self.styleSheet())

        # self.matchScoreField.setText('0:0')
        self.matchScoreField.setPlaceholderText("Saisir le score du match")
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
        self.matchStateField.setCurrentText(matchState)
        self.matchStateField.setContentsMargins(3, 0, 3, 0)
        self.matchStateField.setMinimumWidth(200)
        self.matchStateField.setMaximumWidth(300)

        # Ajout des colonnes dans le add formlayout

        # Groupe Box 1

        # Creation d'un QLabel pour l'image
        self.lbl_img = QLabel()

        self.img = QPixmap("../assets/messi.jpg")

        self.lbl_img.setPixmap(self.img)
        self.lbl_img.setAlignment(Qt.AlignCenter)

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
        self.Hbox = QHBoxLayout()
        self.Vbox.addWidget(self.matchStateLabel)
        self.Vbox.addWidget(self.matchStateField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.matchScoreLabel)
        self.Vbox.addWidget(self.matchScoreField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)
        self.verticalLayout.setAlignment(Qt.AlignCenter)
        # self.verticalLayout.setContentsMargins(10, 0, 10, 0)

        self.update_match_info_button = QPushButton("Modifier", self)
        self.update_match_info_button.setObjectName("btn_primary")
        self.update_match_info_button.setStyleSheet(self.styleSheet())

        self.delete_match_info_button = QPushButton("Supprimer", self)
        self.delete_match_info_button.setObjectName("btn_primary")
        self.delete_match_info_button.setStyleSheet(self.styleSheet())


        self.print_match_info_button = QPushButton("Imprimer", self)
        self.print_match_info_button.setObjectName("btn_primary")
        self.print_match_info_button.setStyleSheet(self.styleSheet())


        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.update_match_info_button)
        self.horizontalLayout.addWidget(self.delete_match_info_button)
        self.horizontalLayout.addWidget(self.print_match_info_button)

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

        self.update_match_info_button.clicked.connect(self.update)
        self.show()

        self.mainLayout.setAlignment(Qt.AlignCenter)

        # Ajout du layout horizontal au layout vertical principal
        self.setLayout(h_layout)

        self.setLayout(self.mainLayout)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Les evenements
        self.update_match_info_button.clicked.connect(lambda: self.update(match_id))
        self.delete_match_info_button.clicked.connect(lambda: self.delete_match(match_id))
        self.print_match_info_button.clicked.connect(lambda: self.print(match_keys, 'match', self.code))

    def update(self,id_match):

            response = MatchController().update_account_info(
                self.typeMatch.currentText(),
                self.countryField.currentText(),
                self.matchDateField.date().toPyDate(),
                self.matchTimeField.text(),
                self.matchTeam1Field.text(),
                self.matchTeam2Field.text(),
                self.matchCoteField.text(),
                self.matchScoreField.text(),
                self.matchStateField.currentText(),
                id_match
            )
            if response == 'update_success':
                QMessageBox.about(self, 'Informations', "Mise a jour effectuee")
                self.close()
                # self.new_match()
                # self.loadDatas()
            else:
                QMessageBox.about(self, 'Erreur', response)

    def delete_match(self,match_id):
        Match().deleteMatch(match_id)
        QMessageBox.about(self, 'valide', "Suppression avec succes !!")
        self.close()


    # Ajout de cette méthode pour centrer la fenêtre
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


    def print(self, keys, table, code=0):

        if code == 0:
            if table == 'match':
                infos = Match().selectMatchInfo()
            elif table == 'user':
                infos = ''
            else:
                infos = ''
        else:
            if table == 'match':
                infos = Match().selectMatchByIdMany(code)
            elif table == 'user':
                infos = User().selectUserByIdMany(code)

        # Load the image file
        logo = QPixmap('assets/LogoBetGee.png')

        # Create a QTextDocument object
        document = QTextDocument()

        # Add the image file to the document as a resource
        document.addResource(QTextDocument.ImageResource, QUrl('logo.png'), logo)

        # Create a QTextCursor for the document
        cursor = QTextCursor(document)

        # Insert the image into the document using the cursor and QTextImageFormat object
        image_format = QTextImageFormat()
        image_format.setName('logo.png')
        cursor.insertImage(image_format)

        # Build the match slip content as a string
        slip = "\t\tGEE BET\n\t\tParye genyen san problem\n\n\n"

        for info in infos:
            match_data = {}
            print('match data :', match_data)
            for key in keys:
                print('key', key)
                value = info[keys.index(key)]
                print('value', value)
                match_data[key] = value
            for key, value in match_data.items():
                slip += "{} : {}\n".format(key, value)
            slip += "+------------------------------------------+\n"

        # Load the bet slip content into the QTextDocument object
        document.setPlainText(slip)

        # Create a QPrinter object
        printer = QPrinter()

        # Create a QPrintDialog object that will show a print dialog
        print_dialog = QtPrintSupport.QPrintDialog(printer)

        # If the user clicks "Print" in the print dialog
        if print_dialog.exec_() == QDialog.Accepted:
            # Print the document
            document.print_(printer)


