from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QHBoxLayout, QLabel,QPushButton, QVBoxLayout, QDialog
from PyQt5.QtGui import QIcon, QTextDocument
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtPrintSupport
from models.Match import Match




class PrintMatchDialog(QDialog):
    def __init__(self, parent, match_id):
        super().__init__(parent)
        self.match_id = match_id
        self.setFixedSize(300, 350)
        self.setStyleSheet(open("../../assets/css/style.css", "r").read())

        # Créer les champs de la fiche de pariage
        self.logo = QPushButton("")
        self.logo.setIcon(QIcon('../../assets/logo_bet_gee.png'))
        self.logo.setIconSize(QSize(64, 64))
        self.logo.setStyleSheet(
            "margin-left: 10px;"
            "border: none;"
        )

        self.match_info = Match().selectMatchById(self.match_id)
        print(self.match_info)


        self.type_match_label = QLabel("Type Match :")
        self.type_match_value = QLabel(self.match_info[1])

        self.country_label = QLabel("Pays :")
        self.country_value = QLabel(self.match_info[2])

        formatted_date = self.match_info[3].strftime("%d/%m/%Y")

        self.match_date_label = QLabel("Date :")
        self.match_date_value = QLabel(formatted_date)

        self.time_match_label = QLabel("Heure :")
        self.time_match_value = QLabel(self.match_info[4])

        self.receiver_team_label = QLabel("Equipe receveuse :")
        self.receiver_team_value = QLabel(self.match_info[5])

        self.visitor_team_label = QLabel("Equipe visiteuse :")
        self.visitor_team_value = QLabel(self.match_info[6])

        self.cote_match_label = QLabel("Cote :")
        self.cote_match_value = QLabel(str(self.match_info[7]))

        self.score_match_label = QLabel("Score")
        self.score_match_value = QLabel(self.match_info[8])

        self.state_match_label = QLabel("Etat")
        self.state_match_value = QLabel(self.match_info[9])


        # Créer un bouton "Imprimer"
        self.print_button = QPushButton("Imprimer")
        self.print_button.setObjectName("print_button")
        self.print_button.setStyleSheet(
            "background-color: #38BDF9;"
            "width: 90px;"
            "border-radius:5px;"
            "padding: 8px;"
        )
        self.print_button.clicked.connect(self.print_bet_slip)

        # Disposer les champs et le bouton dans un layout horizontal
        self.layout_vertical = QVBoxLayout()

        # Disposer les champs et le bouton dans un layout horizontal
        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.logo)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.type_match_label)
        self.horizontal_layout.addWidget(self.type_match_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.country_label)
        self.horizontal_layout.addWidget(self.country_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.match_date_label)
        self.horizontal_layout.addWidget(self.match_date_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.time_match_label)
        self.horizontal_layout.addWidget(self.time_match_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.receiver_team_label)
        self.horizontal_layout.addWidget(self.receiver_team_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.visitor_team_label)
        self.horizontal_layout.addWidget(self.visitor_team_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.cote_match_label)
        self.horizontal_layout.addWidget(self.cote_match_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.score_match_label)
        self.horizontal_layout.addWidget(self.score_match_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.state_match_label)
        self.horizontal_layout.addWidget(self.state_match_value)
        self.layout_vertical.addLayout(self.horizontal_layout)

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.print_button)
        self.horizontal_layout.setAlignment(Qt.AlignCenter)

        self.layout_vertical.addLayout(self.horizontal_layout)

        # Appliquer le layout à la fenêtre
        self.setLayout(self.layout_vertical)

        self.show()



    def print_bet_slip(self):
        # Créer un objet QPrinter
        printer = QPrinter()

        print(id)

        # Créer un objet QTextDocument qui contiendra le contenu à imprimer
        document = QTextDocument()

        # Générer le contenu de la fiche de pariage
        type = self.type_match_value.text()
        country = self.country_value.text()
        date = self.match_date_value.text()
        time = self.time_match_value.text()
        receiver = self.receiver_team_value.text()
        visitor = self.visitor_team_value.text()
        cote = self.cote_match_value.text()
        score = self.score_match_value.text()
        state = self.state_match_value.text()

        # Construire le contenu de la fiche de pariage sous forme de chaîne de caractères
        bet_slip = "Type Match : {}\n".format(type)
        bet_slip += "Pays organisateur : {}\n".format(country)
        bet_slip += "Date: {}\n".format(date)
        bet_slip += "Heure : {}\n".format(time)
        bet_slip += "Equipe receveuse : {}\n".format(receiver)
        bet_slip += "Equipe visiteuse : {}\n".format(visitor)
        bet_slip += "Cote : {}\n".format(cote)
        bet_slip += "Score : {}\n".format(score)
        bet_slip += "Etat : {}\n".format(state)
        bet_slip += "+------------------------------------------+\n"

        # Charger le contenu de la fiche de pariage dans l'objet QTextDocument
        document.setPlainText(bet_slip)

        # Créer un objet QPrintDialog qui affichera une boîte de dialogue d'impression
        print_dialog = QtPrintSupport.QPrintDialog(printer)

        # Si l'utilisateur clique sur "Imprimer" dans la boîte de dialogue d'impression
        if print_dialog.exec_() == QDialog.Accepted:
            # Cacher le bouton "Imprimer"
            self.logo.setVisible(True)
            # Imprimer le document
            document.print_(printer)

