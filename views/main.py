from PyQt5 import QtPrintSupport
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidget, QMainWindow, QGridLayout, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QLineEdit, QTableWidgetItem, QTabBar, QTextEdit
from PyQt5.QtGui import QIcon, QTextDocument, QPixmap, QDoubleValidator
from PyQt5.QtCore import Qt, QSize, QTimer

from models.Retrait import Retrait
from models.User import User
from views.MatchDialog import MatchDialog
from views.PasswordDialog import PasswordDialog
from views.RetraitAccountDialog import RetraitAccountDialog
from views.RechargeAccountDialog import RechargeAccountDialog
from controllers.MatchController import MatchController
from models.RechargeAccount import RechargeAccount
from views.CompteDialog import CompteDialog
from datetime import date
from models.Bet import Bet
from models.Match import Match
from views.addMatch import AddMatch
from models.Payment import Payment
import re
import random
import string

from views.authentification import LoginDialog


class mainView(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bet Gee")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet(open('../assets/css/style.css', "r").read())

        self.showMaximized()
        self.setWindowIcon(QIcon("../assets/LogoBetGee.png"))
        self.container = QGridLayout(self)
        self.pari_data = []
        self.score_prevues = []
        self.id_match_choisi = []
        self.cote_bet = []
        self.rencontre = []
        self.somme_montant = 0.00
        self.index = 0

        # Créer un tableau d'images
        self.images = [
            QPixmap('../assets/goat.jpg'),
            QPixmap("../assets/ronaldo.jpg"),
            QPixmap("../assets/cr7.jpg"),
            QPixmap("../assets/lionelmessi.jpg"),
            QPixmap("../assets/neymar.jpg"),
            QPixmap("../assets/neymarjr.jpg")
        ]

        self.display()
        self.header_content()

        self.bet_info_content()
        self.content = QWidget()

        self.content.setLayout(self.container)
        self.setCentralWidget(self.content)

        self.connection()

    def display(self) -> None:

        self.header = QWidget(self)
        self.header.setObjectName("header")

        self.sidebar = QWidget(self)
        self.sidebar.setObjectName("sidebar")

        self.body = QWidget(self)
        self.body.setObjectName("body")

        self.bet_info = QWidget(self)

        self.bet_info.setObjectName("bet_info")

        self.container.addWidget(self.header, 0, 0, 1, 3)
        self.container.addWidget(self.sidebar, 1, 0)
        self.container.addWidget(self.body, 1, 1, 1, 3)

        if User().display_UserAuth():
            if User().select_userById(User().display_UserAuth())[11] != "admin":
                self.container.addWidget(self.bet_info, 1, 2)

        self.setContentsMargins(0, 0, 0, 0)
        self.container.setRowStretch(0, 1)
        self.container.setRowStretch(1, 8)

        self.container.setColumnStretch(0, 2)
        self.container.setColumnStretch(1, 5)
        self.container.setColumnStretch(2, 2)

        self.container.setSpacing(0)

    def header_content(self):

        # Menu de l'entete
        self.main_layout = QHBoxLayout()
        self.content_layout = QHBoxLayout()

        self.menu = QGroupBox()
        self.menu.setFixedWidth(550)
        self.dark_and_light_mode = QGroupBox()

        self.dark_and_light_mode.setFixedWidth(250)
        self.dark_and_light_mode.setAlignment(Qt.AlignRight)
        self.content_layout_mode = QHBoxLayout()

        # Nom de l'application
        self.app_name = QLabel("BET GEE")
        self.app_name.setObjectName('app_name')
        self.content_layout.addWidget(self.app_name)

        # Bouton pour les matchs
        self.match_btn = QPushButton("Matchs")
        self.match_btn.setObjectName("btn_menu")
        self.match_btn.setStyleSheet(self.styleSheet())

        # Bouton pour les paris
        self.bet_btn = QPushButton("Mes Paris")
        self.bet_btn.setObjectName("btn_menu")
        self.bet_btn.setStyleSheet(self.styleSheet())

        # Bouton pour les paiements
        self.payment_btn = QPushButton("Paiements")
        self.payment_btn.setObjectName("btn_menu")
        self.payment_btn.setStyleSheet(self.styleSheet())

        # Bouton pour les transactions
        self.transaction_btn = QPushButton("Transactions")
        self.transaction_btn.setObjectName("btn_menu")
        self.transaction_btn.setStyleSheet(self.styleSheet())

        # Bouton pour les comptes
        self.disconnect_btn = QPushButton("Deconnexion")
        self.disconnect_btn.setObjectName("btn_disconnect")
        self.disconnect_btn.setStyleSheet(self.styleSheet())

        # Bouton pour le darkmode / lightmode
        self.dark_mode_btn = QPushButton("Darkmode")
        self.dark_mode_btn.setStyleSheet(self.styleSheet())
        self.dark_mode_btn.setObjectName("btn_menu")

        self.lightmode_btn = QPushButton("Lightmode")
        self.lightmode_btn.setStyleSheet(self.styleSheet())
        self.lightmode_btn.setObjectName("btn_menu")

        # Authentification
        self.auth = QGroupBox()

        self.content_layout_auth = QVBoxLayout()
        self.content_h_layout=  QHBoxLayout()

        if User().display_UserAuth():
            self.fullName_user_auth = User().select_userById(User().display_UserAuth())[2] + " " + \
                                      User().select_userById(User().display_UserAuth())[1]
            self.content_profil_btn = User().select_userById(User().display_UserAuth())[2][0] , User().select_userById(User().display_UserAuth())[1][0]
            self.user = QLabel(self.fullName_user_auth)
            self.solde = User().select_userById(User().display_UserAuth())[9]
            self.sold = QLabel(f" Solde : {self.solde} Gourdes")

            # profil button
            self.profil_btn = QPushButton(''.join(self.content_profil_btn))
            self.profil_btn.setObjectName("profil_btn")
            self.content_h_layout.addWidget(self.profil_btn)

            # Ajout des widgets
            self.content_layout_auth.addWidget(self.user)
            self.content_layout_mode.addWidget(self.dark_mode_btn)
            self.content_layout_mode.addWidget(self.lightmode_btn)
            self.profil_btn.clicked.connect(lambda : self.showDialog("profil"))

            if User().select_userById(User().display_UserAuth())[11] != "admin":
                # Ajout des widgets
                self.content_layout.addWidget(self.match_btn)
                self.content_layout.addWidget(self.bet_btn)
                self.content_layout.addWidget(self.payment_btn)
                self.content_layout.addWidget(self.transaction_btn)
                self.content_layout_auth.addWidget(self.sold)
                self.content_h_layout.addLayout(self.content_layout_auth)
            else:
                # Ajout des widgets
                self.content_layout.addWidget(self.app_name)
        else:
            QMessageBox.about(self, 'Erreur', "Pas de session d'utilisateur en cours")

        # Ajout des widgets du content_layout dans le menu
        self.menu.setLayout(self.content_layout)

        self.dark_and_light_mode.setLayout(self.content_layout_mode)

        self.auth.setLayout(self.content_h_layout)

        # Ajout du menu dans le main_layout
        self.main_layout.addWidget(self.menu, alignment=Qt.AlignLeft)

        self.main_layout.addWidget(self.dark_and_light_mode, alignment=Qt.AlignRight)

        # Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.auth, alignment=Qt.AlignRight)

        # Ajout du main_layout dans le header
        self.header.setLayout(self.main_layout)

        # les evenements
        self.match_btn.clicked.connect(self.home_content)
        self.bet_btn.clicked.connect(self.paris_content)
        self.payment_btn.clicked.connect(self.paiement_content)
        self.transaction_btn .clicked.connect(self.transaction_content)
        self.disconnect_btn.clicked.connect(self.disconnect)

    def sidebar_content_admin(self):
        # Menu principal
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Menu principal")

        # Logo de l'application
        self.logo = QPushButton(QIcon('assets/LogoBetGee.png'), "")
        size = QSize(64, 64)
        self.logo.setIconSize(size)

        self.dashboard_btn = QPushButton("Dashboard")
        self.dashboard_btn.setObjectName("btn_menu")
        self.dashboard_btn.setStyleSheet(self.styleSheet())

        self.account_btn = QPushButton("Compte")
        self.account_btn.setObjectName("btn_menu")
        self.account_btn.setStyleSheet(self.styleSheet())

        self.recharge_btn = QPushButton("Recharge")
        self.recharge_btn.setObjectName("btn_menu")
        self.recharge_btn.setStyleSheet(self.styleSheet())

        self.match_btn = QPushButton("Matchs")
        self.match_btn.setObjectName("btn_menu")
        self.match_btn.setStyleSheet(self.styleSheet())

        # Ajout des Widgets
        self.content_layout.addWidget(self.logo)
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.addWidget(self.dashboard_btn)
        self.content_layout.addWidget(self.account_btn)
        self.content_layout.addWidget(self.recharge_btn)
        self.content_layout.addWidget(self.match_btn)

        self.grp.setLayout(self.content_layout)

        # Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.grp, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Informations
        self.content_btm_layout = QVBoxLayout()
        self.grp = QGroupBox()

        self.info_lbl = QLabel("Informations")

        self.password_btn = QPushButton("Mot de passe")
        self.password_btn.setObjectName("btn_menu")
        self.password_btn.setStyleSheet(self.styleSheet())

        self.help_btn = QPushButton("Aide")
        self.help_btn.setObjectName("btn_menu")
        self.help_btn.setStyleSheet(self.styleSheet())

        self.about_btn = QPushButton("A propos")
        self.about_btn.setObjectName("btn_menu")
        self.about_btn.setStyleSheet(self.styleSheet())

        self.disconnect_btn = QPushButton("Deconnexion")
        self.disconnect_btn.setObjectName("btn_disconnect")
        self.disconnect_btn.setStyleSheet(self.styleSheet())

        # Ajout des Widgets
        self.content_btm_layout.addWidget(self.info_lbl)
        self.content_btm_layout.addWidget(self.password_btn)
        self.content_btm_layout.addWidget(self.help_btn)
        self.content_btm_layout.addWidget(self.about_btn)
        self.content_btm_layout.addWidget(self.disconnect_btn)

        # Ajout des composants dans le main_layout
        self.grp.setLayout(self.content_btm_layout)
        self.grp.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.grp, alignment=Qt.AlignBottom)
        self.main_layout.setAlignment(Qt.AlignJustify)

        # Ajout du main_layout dans le sidebar
        self.sidebar.setLayout(self.main_layout)

        # Evenements sur les boutons
        self.dashboard_btn.clicked.connect(self.dashboard_content)
        self.recharge_btn.clicked.connect(lambda: self.showDialog("recharge_solde"))
        self.match_btn.clicked.connect(self.match_content)
        self.account_btn.clicked.connect(self.compte_content)
        self.password_btn.clicked.connect((lambda: self.showDialog("password")))
        self.help_btn.clicked.connect(self.help_content)
        self.about_btn.clicked.connect(self.about_content)
        self.disconnect_btn.clicked.connect(self.disconnect)

    def sidebar_content_parieur(self):
        # Menu principal
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        # Logo de l'application
        self.logo = QPushButton(QIcon('assets/LogoBetGee.png'), "")
        self.logo.setIconSize(QSize(64, 64))

        self.subtitle_lbl = QLabel("Type de matchs")
        self.coupe_du_monde_btn = QPushButton("Coupe Du monde")
        self.coupe_du_monde_btn.setObjectName("btn_menu")
        self.coupe_du_monde_btn.setStyleSheet(self.styleSheet())

        self.championnat_btn = QPushButton("Championnat")
        self.championnat_btn.setObjectName("btn_menu")
        self.championnat_btn.setStyleSheet(self.styleSheet())

        self.eliminatoire_btn = QPushButton("Eliminatoire")
        self.eliminatoire_btn.setObjectName("btn_menu")
        self.eliminatoire_btn.setStyleSheet(self.styleSheet())

        self.amical_btn = QPushButton("Amical")
        self.amical_btn.setObjectName("btn_menu")
        self.amical_btn.setStyleSheet(self.styleSheet())

        # Ajout des Widgets
        self.content_layout.addWidget(self.logo)
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.addWidget(self.coupe_du_monde_btn)
        self.content_layout.addWidget(self.championnat_btn)
        self.content_layout.addWidget(self.eliminatoire_btn)
        self.content_layout.addWidget(self.amical_btn)

        self.grp.setLayout(self.content_layout)
        self.grp.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.grp, alignment=Qt.AlignTop)

        # Informations
        self.content_btm_layout = QVBoxLayout()
        self.grp = QGroupBox()

        self.info_lbl = QLabel("Informations")

        self.setting_btn = QPushButton("Parametres")
        self.setting_btn.setObjectName("btn_menu")
        self.setting_btn.setStyleSheet(self.styleSheet())

        self.help_btn = QPushButton("Aide")
        self.help_btn.setObjectName("btn_menu")
        self.help_btn.setStyleSheet(self.styleSheet())

        self.about_btn = QPushButton("A propos")
        self.about_btn.setObjectName("btn_menu")
        self.about_btn.setStyleSheet(self.styleSheet())

        self.retrait_btn = QPushButton("Retrait")
        self.retrait_btn.setObjectName("btn_menu")
        self.retrait_btn.setStyleSheet(self.styleSheet())

        self.disconnect_btn = QPushButton("Deconnexion")
        self.disconnect_btn.setObjectName("btn_disconnect")
        self.disconnect_btn.setStyleSheet(self.styleSheet())

        # Ajout des Widgets
        self.content_btm_layout.addWidget(self.info_lbl)
        self.content_btm_layout.addWidget(self.setting_btn)
        self.content_btm_layout.addWidget(self.help_btn)
        self.content_btm_layout.addWidget(self.about_btn)
        self.content_btm_layout.addWidget(self.retrait_btn)
        self.content_btm_layout.addWidget(self.disconnect_btn)

        # Ajout des composants dans le main_layout
        self.grp.setLayout(self.content_btm_layout)

        self.main_layout.addWidget(self.grp, alignment=Qt.AlignBottom)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Ajout du main_layout dans le sidebar
        self.sidebar.setLayout(self.main_layout)

        # Evenement
        self.retrait_btn.clicked.connect(lambda : self.showDialog("retrait"))
        self.disconnect_btn.clicked.connect(self.disconnect)


    def bet_info_content(self):

        # Menu principal
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        for i in range(len(self.pari_data)):
            self.box = QGroupBox()
            self.content_box = QVBoxLayout()
            self.box.setLayout(self.content_box)

            self.subtitle_lbl = QLabel("Informations du pariage :")
            self.close_btn = QPushButton("Retirer")
            self.close_btn.setObjectName("btn_disconnect")
            self.close_btn.setFixedWidth(100)
            self.recontre_lbl = QLabel(
                f"Recontre : {self.pari_data[i]['receiver_team']} VS {self.pari_data[i]['visitor_team']}")
            self.cote_lbl = QLabel(f"cote : {self.pari_data[i]['cote']}")

            self.content_box.addWidget(self.close_btn, alignment=Qt.AlignRight)
            self.content_box.addWidget(self.subtitle_lbl)
            self.content_box.addWidget(self.recontre_lbl)
            self.content_box.addWidget(self.cote_lbl)

            self.score_prevus_lbl = QLabel("Saisissez le score prevus")
            self.score_prevus_field = QLineEdit()
            self.score_prevus_field.setPlaceholderText("Format : 2:0")
            self.score_prevus_field.setObjectName("fields")
            self.score_prevus_field.setStyleSheet(self.styleSheet())
            self.content_box.addWidget(self.score_prevus_lbl)
            self.content_box.addWidget(self.score_prevus_field)
            self.score_prevues.append(self.score_prevus_field)
            self.id_match_choisi.append(self.pari_data[i]['id'])
            self.cote_bet.append(self.pari_data[i]['cote'])
            self.rencontre.append({"receiver_team": self.pari_data[i]['receiver_team'],
                                   "visitor_team": self.pari_data[i]['visitor_team']})

            self.content_layout.addWidget(self.box)

            # evenement
            self.close_btn.clicked.connect((lambda i: lambda: self.delete_item_pari(self.pari_data[i]['id']))(i))

        doubleVal = QDoubleValidator()
        self.bet_amount_lbl = QLabel("Montant du pariage : ")
        self.bet_amount_field = QLineEdit()
        self.bet_amount_field.setValidator(doubleVal)
        self.bet_amount_field.setObjectName("fields")
        self.bet_amount_field.setStyleSheet(self.styleSheet())
        self.bet_amount_field.setText(f"{0.00}")

        self.parier_btn = QPushButton("Parier")
        self.parier_btn.setObjectName("btn_primary")
        self.parier_btn.setStyleSheet(self.styleSheet())

        self.bet_h_layout = QHBoxLayout()
        self.bet_win_h_layout = QHBoxLayout()

        self.total_lbl = QLabel("Cote Total : ")
        self.total_value_lbl = QLabel(str(self.somme_cote()))
        self.total_value_lbl.setObjectName("fields")
        self.total_value_lbl.setStyleSheet(self.styleSheet())

        self.bet_win_lbl = QLabel("Possibilite de gain de : ")
        self.bet_win_value_lbl = QLabel(f"{self.somme_montant} Gourdes")
        self.bet_win_value_lbl.setObjectName("fields")
        self.bet_win_value_lbl.setStyleSheet(self.styleSheet())

        self.bet_amount_field.textChanged.connect(self.on_text_changed)
        self.bet_amount_field.setObjectName("fields")
        self.bet_amount_field.setStyleSheet(self.styleSheet())

        # Ajout des Widgets

        self.content_layout.addWidget(self.bet_amount_lbl)
        self.content_layout.addWidget(self.bet_amount_field)
        self.content_layout.addWidget(self.parier_btn)

        self.bet_h_layout.addWidget(self.total_lbl)
        self.bet_h_layout.addWidget(self.total_value_lbl)

        self.bet_win_h_layout.addWidget(self.bet_win_lbl)
        self.bet_win_h_layout.addWidget(self.bet_win_value_lbl)

        self.content_layout.addLayout(self.bet_h_layout)
        self.content_layout.addLayout(self.bet_win_h_layout)

        self.grp.setLayout(self.content_layout)
        self.grp.setContentsMargins(5, 5, 5, 5)

        # Ajout des composants dans le main_layout
        self.main_layout.addWidget(self.grp, alignment=Qt.AlignTop)

        self.main_layout.setAlignment(Qt.AlignJustify)

        # Ajout du main_layout dans le sidebar
        self.bet_info.setLayout(self.main_layout)

        # Evenements sur les boutons
        self.parier_btn.clicked.connect(lambda: self.placerPari())

    def dashboard_content(self):

        # Contenu du dashboard
        self.content_layout = QVBoxLayout()

        self.lbl = QLabel("Welcome to your dashboard")

        # Créez un widget principal et définissez sa disposition en utilisant un QVBoxLayout
        widget = QWidget()
        widget.setLayout(self.content_layout)

        # Créez le premier QGroupBox et définissez sa disposition en utilisant un QHBoxLayout
        groupBox1 = QGroupBox("GroupBox 1")
        groupBox1.setObjectName("statistic")
        layout1 = QHBoxLayout()
        groupBox1.setLayout(layout1)

        # Ajoutez les widgets que vous voulez inclure dans le premier QGroupBox au QHBoxLayout
        label1 = QLabel("Label 1")
        layout1.addWidget(label1)

        # Créez les deux autres QGroupBox et définissez leur disposition en utilisant un QHBoxLayout pour chacun d'eux
        groupBox2 = QGroupBox("GroupBox 2")
        groupBox2.setObjectName("statistic")

        layout2 = QVBoxLayout()
        groupBox2.setLayout(layout2)

        groupBox3 = QGroupBox("GroupBox 3")
        groupBox3.setObjectName("statistic")
        layout3 = QVBoxLayout()
        groupBox3.setLayout(layout3)

        # Ajoutez les widgets que vous voulez inclure dans chaque QGroupBox au QHBoxLayout correspondant
        label2 = QLabel("Label 2")
        layout2.addWidget(label2)

        label3 = QLabel("Label 3")
        layout3.addWidget(label3)

        # Ajout des Widgets
        # Ajoutez les trois QGroupBox au QVBoxLayout principal

        self.content_layout.addWidget(self.lbl)
        self.content_layout.addWidget(groupBox1)
        self.content_layout.addWidget(groupBox2)
        self.content_layout.addWidget(groupBox3)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.change_body_content()
        self.body.setLayout(self.content_layout)

    def compte_content(self):

        self.header = (
            "Code", "Nom", "Prenom", "Nom Ut", "Date de nais", "Sexe", "Tel", "Nif/Cin", "Mot de passe", "Solde",
            "Statut",
            "Type Ut")

        account_keys = list(self.header)

        # Contenu du dashboard
        self.content_layout = QVBoxLayout()

        self.grp_box_account_btn = QGroupBox()

        self.info_lbl = QLabel('Imprimez les comptes de vos utilisateurs par ici')
        self.print_compte_info_button = QPushButton("Imprimer")
        self.print_compte_info_button.setObjectName("btn_primary")
        self.print_compte_info_button.setFixedWidth(150)

        self.print_compte_info_button.setStyleSheet(self.styleSheet())

        self.content_layout.addWidget(self.info_lbl)
        self.content_layout.addWidget(self.print_compte_info_button)

        self.grp_box_account_btn.setLayout(self.content_layout)
        self.grp_box_account_btn.setAlignment(Qt.AlignCenter)

        self.content_layout = QVBoxLayout()

        # create_match_table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.header))
        self.table.setHorizontalHeaderLabels(self.header)
        self.table.setObjectName("table")
        window_width = self.table.size().width()

        column_width = window_width // len(self.header) * 2 - 22

        for i in range(len(self.header)):
            self.table.setColumnWidth(i, column_width)

        self.table.cellClicked.connect(self.userTableEvent)

        self.content_layout.addWidget(self.grp_box_account_btn)
        self.content_layout.addWidget(self.table)
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.loadDataUser()

        # Ajout des composants dans le body layout
        self.change_body_content()
        self.body.setLayout(self.content_layout)

        self.print_compte_info_button.clicked.connect(lambda: self.print(account_keys, 'user'))

    def match_content(self):
        self.header = (
            "Id", "Type Match", "Pays", "Date Match", "Heure Match", "Equipe Receveuse", "Equipe Visiteuse", "Cote",
            "Score", "Etat")

        self.matchs_keys = list(self.header)

        # Contenu du dashboard
        self.grp_box_match_btn = QGroupBox()
        self.content_layout = QVBoxLayout()
        self.content_layout_h = QHBoxLayout()

        self.save_match_info_button = QPushButton("Enregistrer Match")
        self.save_match_info_button.setObjectName("btn_primary")
        self.save_match_info_button.setStyleSheet(self.styleSheet())

        self.print_match_info_button = QPushButton("Imprimer")
        self.print_match_info_button.setObjectName("btn_primary")
        self.print_match_info_button.setStyleSheet(self.styleSheet())

        self.save_match_info_button.setFixedWidth(150)
        self.print_match_info_button.setFixedWidth(150)

        # create_match_table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.header))
        self.table.setHorizontalHeaderLabels(self.header)
        self.table.setObjectName("table")
        window_width = self.table.size().width()

        column_width = window_width // len(self.header) * 2 - 22

        for i in range(len(self.header)):
            self.table.setColumnWidth(i, column_width)

        self.table.cellClicked.connect(self.matchTableEvent)

        self.content_layout_h.addWidget(self.save_match_info_button)
        self.content_layout_h.addWidget(self.print_match_info_button)
        self.content_layout.addLayout(self.content_layout_h)

        self.grp_box_match_btn.setLayout(self.content_layout)
        self.grp_box_match_btn.setAlignment(Qt.AlignCenter)

        self.content_layout.addWidget(self.table)
        self.loadMatchDatas()

        # Ajout des composants dans le main_layout
        self.change_body_content()
        self.body.setLayout(self.content_layout)

        # les evenement
        self.save_match_info_button.clicked.connect(lambda: self.showDialog("add_match"))
        self.print_match_info_button.clicked.connect(lambda: self.print(self.matchs_keys, 'match'))

        # Appel de la fonction print_match avec les cles

    def print(self, keys, table, code=0):

        if code == 0:
            if table == 'match':
                infos = Match().selectMatchInfo()
            elif table == 'user':
                infos = User().selectUserInfo()
            elif table == 'bet':
                infos = Bet().selectBetInfo()
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
        #
        # # Add the image file to the document as a resource
        # document.addResource(QTextDocument.ImageResource, QUrl('logo.png'), logo)
        #
        # # Create a QTextCursor for the document
        # cursor = QTextCursor(document)
        #
        # # Insert the image into the document using the cursor and QTextImageFormat object
        # image_format = QTextImageFormat()
        # image_format.setName('logo.png')
        # cursor.insertImage(image_format)

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
            # Hide the "Print" button
            self.logo.setVisible(True)
            # Print the document
            document.print_(printer)

    def connection(self):
        if User().display_UserAuth():
            if User().select_userById(User().display_UserAuth())[11] != "admin":
                self.sidebar_content_parieur()
                self.home_content()
            else:
                self.sidebar_content_admin()
                self.dashboard_content()
        else:
            self.close()
            LoginDialog(self).showLogin()

    def setting_content(self):

        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Welcome to your setting info")

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.change_body_content()
        self.body.setLayout(self.content_layout)

    def help_content(self):

        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("How can we help you ?")

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.change_body_content()
        self.body.setLayout(self.content_layout)

    def about_content(self):

        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        # Menu principal
        self.main_layout = QVBoxLayout()
        self.content_v_layout = QVBoxLayout()
        self.content_h_layout = QHBoxLayout()
        self.grp = QGroupBox()

        self.about_lbl = QLabel("A propos de nous")
        self.about_lbl.setAlignment(Qt.AlignCenter)
        self.about_txt = QTextEdit(""
                                   "Notre groupe de programmeurs est composé de développeurs expérimentés en Python et PyQt5,"
                                   " qui ont décidé de collaborer sur un projet de pari de match en ligne. Nous avons choisi de utiliser Python "
                                   "comme langage de programmation principal car c'est un langage polyvalent et populaire qui nous permet de développer"
                                   " rapidement des applications de qualité. Nous avons également choisi d'utiliser PyQt5, une bibliothèque de graphiques en Python, "
                                   "pour créer une interface utilisateur attrayante et intuitive.Le projet consiste à développer une plateforme en ligne où les utilisateurs "
                                   "pourront parier sur les résultats de matchs de football. Nous avons défini les fonctionnalités de base de notre application, telles que "
                                   "l'inscription et la connexion des utilisateurs, la visualisation des matchs et des cotes, la placement des paris et le suivi des gains et pertes."
                                   " Nous avons également prévu de mettre en place un système de gestion des utilisateurs et de la sécurité pour protéger les données des utilisateurs "
                                   "et garantir la confidentialité.Nous travaillons en étroite collaboration pour développer cette application de manière efficace et en respectant les délais "
                                   "que nous nous sommes fixés. Nous nous appuyons sur nos compétences en Python et PyQt5, ainsi que sur notre expérience de travail en équipe, pour atteindre "
                                   "nos objectifs. Nous sommes impatients de voir notre projet aboutir et de le mettre en ligne pour que les utilisateurs puissent en profiter.")
        self.about_txt.setAlignment(Qt.AlignCenter)
        self.about_txt.setFixedHeight(500)

        # Ajout des Widgets
        self.content_layout.addWidget(self.about_lbl)
        self.content_layout.addWidget(self.about_txt)
        self.content_layout.setAlignment(Qt.AlignCenter)

        self.content_layout.addLayout(self.content_v_layout)

        # Ajout des composants dans le main_layout
        self.grp.setLayout(self.content_h_layout)
        self.grp.setFixedSize(self.body.size().width() - 50, self.body.size().height() - 50)
        self.grp.setObjectName("match_info_grp")
        self.grp.setAlignment(Qt.AlignCenter)

        self.content_layout.addWidget(self.grp, alignment=Qt.AlignCenter)

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.change_body_content()
        self.body.setLayout(self.content_layout)

    def home_content(self):
        # Contenu du dashboard
        self.Vbox = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        # Créer un timer qui se déclenchera toutes les 3 secondes
        self.timer = QTimer(self)
        self.timer.setInterval(3000)  # en millisecondes
        self.timer.timeout.connect(self.afficher_image)

        # Image pour le slideshow
        self.group_box_image = QGroupBox()
        self.group_box_image.setFixedSize(800, 400)
        self.vertical_box_image = QVBoxLayout()
        self.hor_box_image = QVBoxLayout()
        self.label_image = QLabel()
        self.label_image.setScaledContents(True)
        # setScaledContents()

        self.group_box_image.setFixedSize(self.label_image.width(), 300)

        self.label_image.setPixmap(self.images[0])

        self.vertical_box_image.addWidget(self.label_image)

        self.group_box_image.setLayout(self.vertical_box_image)
        self.group_box_image.setAlignment(Qt.AlignCenter)

        # Démarrer le timer
        self.timer.start()

        # self.grp = QGroupBox()
        id_match = []
        match_type = []
        country = []
        date_match = []
        time_match = []
        eq1 = []
        eq2 = []
        score = []
        cote = []
        status = []

        for i in range(len(MatchController().displayMatch())):
            id_match.append(MatchController().displayMatch()[i][0])
            match_type.append(MatchController().displayMatch()[i][1])
            country.append(MatchController().displayMatch()[i][2])
            date_match.append(MatchController().displayMatch()[i][3])
            time_match.append(MatchController().displayMatch()[i][4])
            eq1.append(MatchController().displayMatch()[i][5])
            eq2.append(MatchController().displayMatch()[i][6])
            cote.append(MatchController().displayMatch()[i][7])
            score.append(MatchController().displayMatch()[i][8])
            status.append(MatchController().displayMatch()[i][9])



            self.box = QGroupBox()
            self.content_box = QVBoxLayout()
            self.box.setFixedWidth(700)
            self.box.setFixedHeight(100)
            self.box.setLayout(self.content_box)

            self.grpbx_entete_match = QGroupBox()
            self.grpbx_info_match = QGroupBox()
            self.grpbx_entete_match.setObjectName("border")
            self.hbox_layout = QHBoxLayout()
            self.vbox_layout = QVBoxLayout()

            self.type_match_lbl = QLabel("Championnat")
            self.country_lbl = QLabel(f"Pays receveuse : {country[i]}")
            self.cote_lbl = QLabel("Cote : 1.4")

            self.vbox_layout.addWidget(self.type_match_lbl)
            self.vbox_layout.setAlignment(Qt.AlignLeft)

            self.vbox_layout.addWidget(self.country_lbl)
            self.vbox_layout.addWidget(self.cote_lbl)
            self.hbox_layout.addLayout(self.vbox_layout)
            self.vbox_layout = QVBoxLayout()


            print(match_type[i])

            if status[i] == "T":
                self.score_lbl = QLabel(f"{score[i]}")
                self.score_lbl.setStyleSheet("font-size: 20px;")
                self.state_lbl = "Termine"
                self.vbox_layout.addWidget(self.score_lbl)
            else:
                self.state_lbl = "VS"
                # self.vbox_layout.addWidget(self.vs)

            self.match = QLabel(f"{eq1[i]} {self.state_lbl} {eq2[i]}")

            self.hbox_layout.addWidget(self.match)

            self.hbox_layout.addLayout(self.vbox_layout)

            self.hbox_layout.addLayout(self.vbox_layout)

            self.grpbx_entete_match.setLayout(self.hbox_layout)
            # self.grpbx_entete_match.setStyleSheet("color: black;")

            self.hbox_layout = QHBoxLayout()

            date_to_str = date_match[0]

            self.date = QLabel(f"{date_to_str}")
            self.time = QLabel(f"{time_match[0]}")
            self.score = QLabel(f"{score[0]}")
            self.cote = QLabel(f"{cote[0]}")

            # self.grpbx_entete_match.setLayout(self.hbox_layout)
            self.grpbx_entete_match.setAlignment(Qt.AlignCenter)
            # self.vbox_layout_value = QHBoxLayout()

            self.add = QPushButton("Ajouter")
            self.add.setObjectName("btn_primary")
            self.add.setStyleSheet(self.styleSheet())
            self.add.setFixedWidth(150)

            # self.Vbox.addWidget(self.grpbx_info_match)
            self.Vbox.addWidget(self.grpbx_entete_match)
            self.Vbox.addWidget(self.add)

            # evenement
            # Ajout d'un événement de clic en utilisant une closure
            self.add.clicked.connect(
                (lambda i: lambda: self.add_data_pari(id_match[i], eq1[i], eq2[i], cote[i]))(i))

        self.content_layout.addWidget(self.group_box_image, Qt.AlignCenter)
        self.content_layout.addLayout(self.Vbox)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.change_body_content2()
        self.body.setLayout(self.content_layout)

    def paris_content(self):
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Mes paris")
        self.subtitle_lbl.setStyleSheet("font-size: 18px; padding: 10px;")

        # Création de la barre d'onglets
        self.tab_bar = QTabBar()
        self.tab_bar.setContentsMargins(30, 0, 30, 0)

        # Ajout d'onglets à la barre d'onglets
        self.tab_bar.addTab("Tout")
        self.tab_bar.addTab("Gagne")
        self.tab_bar.addTab("Perdu")

        # Création des widgets de contenu

        # content all pari
        self.tab1 = QGroupBox()
        self.content_box = QVBoxLayout()
        self.tab1.setFixedWidth(700)
        self.tab1.setLayout(self.content_box)

        if Bet().selectBetByUserId(User().display_UserAuth()):
            id = []
            for i in range(len(Bet().selectBetByUserId(User().display_UserAuth()))):
                print(Bet().displayMatchByBetCode(Bet().selectBetByUserId(User().display_UserAuth())[i][1]))
                # header
                if Bet().selectBetByUserId(User().display_UserAuth())[i][1] not in id:
                    id.append(Bet().selectBetByUserId(User().display_UserAuth())[i][1])
                    self.code_pariage = QLabel(f"Code : {Bet().selectBetByUserId(User().display_UserAuth())[i][1]}")
                    self.bet_date = QLabel(f"Date : {Bet().selectBetByUserId(User().display_UserAuth())[i][3]}")
                    self.bet_amount = QLabel(f"Montant : {Bet().selectBetByUserId(User().display_UserAuth())[i][4]}")
                    self.content_box.addWidget(self.code_pariage)
                    self.content_box.addWidget(self.bet_date)
                    self.content_box.addWidget(self.bet_amount)
                    for element in Bet().displayMatchByBetCode(
                            Bet().selectBetByUserId(User().display_UserAuth())[i][1]):
                        # #body
                        self.equipe_choisielbl = QLabel(f"Equipe choisie : {element[3]}")
                        self.cotebet_lbl = QLabel(f"Cote : {element[3]}")
                        self.score_prevulbl = QLabel(f"score prevu : {element[5]}")
                        self.etat_pariage = QLabel(f"Status : {element[6]}")
                        self.content_box.addWidget(self.equipe_choisielbl)
                        self.content_box.addWidget(self.cotebet_lbl)
                        self.content_box.addWidget(self.score_prevulbl)
                        self.content_box.addWidget(self.etat_pariage)

        self.print_match_info_button = QPushButton("Imprimer")
        self.print_match_info_button.setObjectName("btn_primary")
        self.print_match_info_button.setStyleSheet(self.styleSheet())
        self.content_box.addWidget(self.print_match_info_button)

        # content pari Gagne
        self.tab2 = QGroupBox()
        self.content_box = QVBoxLayout()
        self.tab2.setFixedWidth(700)
        self.tab2.setLayout(self.content_box)

        if Bet().selectBetByUserId(User().display_UserAuth()):
            id = []
            for i in range(len(Bet().selectBetByUserId(User().display_UserAuth()))):
                # header
                if Bet().selectBetByUserId(User().display_UserAuth())[i][1] not in id and not any(
                        'Perdu' in item for item in
                        Bet().displayMatchByBetCode(Bet().selectBetByUserId(User().display_UserAuth())[i][1])):
                    id.append(Bet().selectBetByUserId(User().display_UserAuth())[i][1])
                    self.code_pariage = QLabel(f"Code : {Bet().selectBetByUserId(User().display_UserAuth())[i][1]}")
                    self.bet_date = QLabel(f"Date : {Bet().selectBetByUserId(User().display_UserAuth())[i][3]}")
                    self.bet_amount = QLabel(f"Montant : {Bet().selectBetByUserId(User().display_UserAuth())[i][4]}")
                    self.content_box.addWidget(self.code_pariage)
                    self.content_box.addWidget(self.bet_date)
                    self.content_box.addWidget(self.bet_amount)
                    for element in Bet().displayMatchByBetCode(
                            Bet().selectBetByUserId(User().display_UserAuth())[i][1]):
                        # #body
                        self.equipe_choisielbl = QLabel(f"Equipe choisie : {element[3]}")
                        self.cotebet_lbl = QLabel(f"Cote : {element[3]}")
                        self.score_prevulbl = QLabel(f"score prevu : {element[5]}")
                        self.etat_pariage = QLabel(f"Status : {element[6]}")
                        self.content_box.addWidget(self.equipe_choisielbl)
                        self.content_box.addWidget(self.cotebet_lbl)
                        self.content_box.addWidget(self.score_prevulbl)
                        self.content_box.addWidget(self.etat_pariage)

        self.print_match_info_button = QPushButton("Imprimer")
        self.print_match_info_button.setObjectName("btn_primary")
        self.print_match_info_button.setStyleSheet(self.styleSheet())
        self.content_box.addWidget(self.print_match_info_button)

        # content pari perdu
        self.tab3 = QGroupBox()
        self.content_box = QVBoxLayout()
        self.tab3.setFixedWidth(700)
        self.tab3.setLayout(self.content_box)

        if Bet().selectBetByUserId(User().display_UserAuth()):
            id = []
            for i in range(len(Bet().selectBetByUserId(User().display_UserAuth()))):
                # header
                if Bet().selectBetByUserId(User().display_UserAuth())[i][1] not in id and any(
                        'Perdu' in item for item in
                        Bet().displayMatchByBetCode(Bet().selectBetByUserId(User().display_UserAuth())[i][1])):
                    id.append(Bet().selectBetByUserId(User().display_UserAuth())[i][1])
                    self.code_pariage = QLabel(f"Code : {Bet().selectBetByUserId(User().display_UserAuth())[i][1]}")
                    self.bet_date = QLabel(f"Date : {Bet().selectBetByUserId(User().display_UserAuth())[i][3]}")
                    self.bet_amount = QLabel(f"Montant : {Bet().selectBetByUserId(User().display_UserAuth())[i][4]}")
                    self.content_box.addWidget(self.code_pariage)
                    self.content_box.addWidget(self.bet_date)
                    self.content_box.addWidget(self.bet_amount)
                    for element in Bet().displayMatchByBetCode(
                            Bet().selectBetByUserId(User().display_UserAuth())[i][1]):
                        # #body
                        self.equipe_choisielbl = QLabel(f"Equipe choisie : {element[3]}")
                        self.cotebet_lbl = QLabel(f"Cote : {element[3]}")
                        self.score_prevulbl = QLabel(f"score prevu : {element[5]}")
                        self.etat_pariage = QLabel(f"Status : {element[6]}")
                        self.content_box.addWidget(self.equipe_choisielbl)
                        self.content_box.addWidget(self.cotebet_lbl)
                        self.content_box.addWidget(self.score_prevulbl)
                        self.content_box.addWidget(self.etat_pariage)

        self.print_match_info_button = QPushButton("Imprimer")
        self.print_match_info_button.setObjectName("btn_primary")
        self.print_match_info_button.setStyleSheet(self.styleSheet())
        self.content_box.addWidget(self.print_match_info_button)

        # Création du layout principal
        self.layout = QVBoxLayout()
        self.bet_keys = list(["Code", "Date", "Montant", "Equipe Choisie", "Cote", "Score prevu", "Statut"])
        # Masquage des widgets de contenu
        self.tab1.show()
        self.tab2.hide()
        self.tab3.hide()

        # # Définition du layout principal de la fenêtre
        # self.setLayout(self.layout)

        # self.print_match_info_button.clicked.connect(lambda: self.print(self.bet_keys, 'bet'))

        # Ajout des Widgets
        self.content_layout.addWidget(self.subtitle_lbl)

        # Ajout de la barre d'onglets et des widgets de contenu au layout
        self.content_layout.addWidget(self.tab_bar)
        self.content_layout.addWidget(self.tab1)
        self.content_layout.addWidget(self.tab2)
        self.content_layout.addWidget(self.tab3)

        self.content_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.change_body_content2()
        self.body.setLayout(self.content_layout)
        # self.body.setStyleSheet("background-color: #D6DBDF; color: black;")
        # Connexion du signal "onglet actif changé" à la méthode de changement de contenu
        self.tab_bar.currentChanged.connect(self.change_tab_content)

    def change_tab_content(self, index):
        # Masquage de tous les widgets de contenu
        self.tab1.hide()
        self.tab2.hide()
        self.tab3.hide()

        # Affichage du widget de contenu correspondant à l'onglet sélectionné
        if index == 0:
            self.tab1.show()
        elif index == 1:
            self.tab2.show()
        elif index == 2:
            self.tab3.show()

    def paiement_content(self):
        # Contenu du dashboard
        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        self.grp = QGroupBox()

        self.subtitle_lbl = QLabel("Paiement")
        # Ajout des Widgets
        # self.content_layout.addWidget(self.subtitle_lbl,alignment=Qt.AlignCenter)

        if Payment().selectPaymentInfo():
            for i in range(len(Payment().selectPaymentInfo())):
                self.box=QGroupBox()
                self.box.setFixedHeight(100)
                self.vbox_layout=QVBoxLayout()
                self.box.setLayout(self.vbox_layout)
                self.bet_code_lbl = QLabel(f"Code Pariage : {Payment().selectPaymentInfo()[i][1]}")
                self.payment_date_lbl = QLabel(f"Date Paiement : {Payment().selectPaymentInfo()[i][2]}")
                self.montant_payment_lbl = QLabel(f"Montant Paie : {Payment().selectPaymentInfo()[i][3]}")
                self.vbox_layout.addWidget(self.bet_code_lbl)
                self.vbox_layout.addWidget(self.payment_date_lbl)
                self.vbox_layout.addWidget(self.montant_payment_lbl)
                self.content_layout.addWidget(self.box)

        # Ajout des composants dans le main_layout
        self.change_body_content2()
        self.body.setLayout(self.content_layout)

    def transaction_content(self):

        self.main_layout = QVBoxLayout()
        self.content_layout = QVBoxLayout()

        # Création de la barre d'onglets
        self.tab_bar = QTabBar()
        self.tab_bar.setContentsMargins(30, 0, 30, 0)

        # Ajout d'onglets à la barre d'onglets
        self.tab_bar.addTab(QIcon('assets/bet.svg'), "Depot")
        self.tab_bar.addTab(QIcon('assets/bet.svg'), "Retrait")

        self.onglet1 = QGroupBox()
        # depot
        self.content_box = QVBoxLayout()
        self.onglet1.setFixedWidth(700)
        self.onglet1.setLayout(self.content_box)

        if RechargeAccount().selectRechargeInfo():
            for i in range(len(RechargeAccount().selectRechargeInfo())):
                self.code_user_depot=QLabel(f"code Parieur : {RechargeAccount().selectRechargeInfo()[0][1]}")
                self.content_box.addWidget(self.code_user_depot)
                self.amount_depot=QLabel(f"Montant Deposer : {RechargeAccount().selectRechargeInfo()[0][2]}")
                self.content_box.addWidget(self.amount_depot)
                self.date_depot=QLabel(f"Date Depot : {RechargeAccount().selectRechargeInfo()[0][3]}")
                self.content_box.addWidget(self.date_depot)




        self.onglet2 = QGroupBox()
        # retrait
        self.content_box = QVBoxLayout()
        self.onglet2.setFixedWidth(700)
        self.onglet2.setLayout(self.content_box)

        if Retrait().selectRetraitInfo():
            for i in range(len(Retrait().selectRetraitInfo())):
                self.code_user_retirer=QLabel(f"code Parieur :  {Retrait().selectRetraitInfo()[i][1]}")
                self.content_box.addWidget(self.code_user_retirer)
                self.amount_retirer=QLabel(f"Montant Retirer : {Retrait().selectRetraitInfo()[i][2]}")
                self.content_box.addWidget(self.amount_retirer)
                self.date_retirer=QLabel(f"Date Retirer : {Retrait().selectRetraitInfo()[i][3]}")
                self.content_box.addWidget(self.date_retirer)

        # Ajout de la barre d'onglets et des widgets de contenu au layout
        self.content_layout.addWidget(self.tab_bar)
        self.content_layout.addWidget(self.onglet1)
        self.content_layout.addWidget(self.onglet2)

        self.content_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Ajout des composants dans le main_layout
        self.change_body_content2()
        self.body.setLayout(self.content_layout)
        # self.body.setStyleSheet("background-color: #D6DBDF; color: black;")
        # Connexion du signal "onglet actif changé" à la méthode de changement de contenu
        self.tab_bar.currentChanged.connect(self.change_tab_content2)

    def change_tab_content2(self, index):
            # Masquage de tous les widgets de contenu
            self.onglet1.hide()
            self.onglet2.hide()

            # Affichage du widget de contenu correspondant à l'onglet sélectionné
            if index == 0:
                self.onglet1.show()
            elif index == 1:
                self.onglet2.show()


    def afficher_image(self):

        try:
            # Récupérer l'image actuelle
            pixmap = self.label_image.pixmap()
            if pixmap and not pixmap.isNull():
                # Mettre à jour l'index
                self.index = (self.index + 1) % len(self.images)
            else:
                # Aucune image n'est définie dans le label
                self.index = 0

            # Afficher la prochaine image sans effet de transition
            self.label_image.setPixmap(self.images[self.index])
        except:
            print()

    def disconnect(self):
        User().truncate_userAuth()
        self.close()
        LoginDialog(self).showLogin()

    def change_body_content(self):
        self.body.deleteLater()
        self.body = QWidget(self)
        self.container.addWidget(self.body, 1, 1, 1, 3)

    def change_body_content2(self):
        self.body.deleteLater()
        self.body = QWidget(self)
        self.container.addWidget(self.body, 1, 1)

    def change_bet_info(self):
        self.score_prevues = []
        self.id_match_choisi = []
        self.bet_info.deleteLater()
        self.bet_info = QWidget(self)
        self.bet_info.setObjectName("bet_info")
        self.container.addWidget(self.bet_info, 1, 2)

    def change_header(self):
        self.header.deleteLater()
        self.header = QWidget(self)
        self.container.addWidget(self.header, 0, 0, 1, 3)
        self.header.setStyleSheet(
            "background-color: #151515;"
        )
        self.header_content()

    def showDialog(self, dialog):
        if dialog == "recharge_solde":
            recharge_dialog = RechargeAccountDialog(self)
            result = recharge_dialog.exec_()
            if result == QDialog.Rejected:
                self.change_body_content()
                self.compte_content()
        if dialog == "retrait":
                retrait_dialog = RetraitAccountDialog(self,User().select_userById(User().display_UserAuth())[0])
                result = retrait_dialog.exec_()
                if result == QDialog.Rejected:
                    self.change_header()
                    self.header_content()
        elif dialog == "add_match":
            addMatch_dialog = AddMatch(self)
            result = addMatch_dialog.exec_()
            if result == QDialog.Rejected:
                self.change_body_content()
                self.match_content()
        elif dialog == 'profil':
            compte_dialog = CompteDialog(self, User().select_userById(User().display_UserAuth())[0],
                                                User().select_userById(User().display_UserAuth())[1],
                                         User().select_userById(User().display_UserAuth())[2],
                                         User().select_userById(User().display_UserAuth())[3],
                                         User().select_userById(User().display_UserAuth())[4].strftime("%Y-%m-%d"),
                                         User().select_userById(User().display_UserAuth())[5],
                                         User().select_userById(User().display_UserAuth())[6],
                                         User().select_userById(User().display_UserAuth())[7],
                                         User().select_userById(User().display_UserAuth())[8],
                                         User().select_userById(User().display_UserAuth())[9],
                                         User().select_userById(User().display_UserAuth())[10],
                                         User().select_userById(User().display_UserAuth())[11])
            result = compte_dialog.exec_()
            if result == QDialog.Rejected:
                self.change_header()
                self.header_content()
        elif dialog == 'password':
            PasswordDialog(self, User().select_userById(User().display_UserAuth())).show()

    def loadMatchDatas(self):
        lignes = MatchController().displayMatch()
        self.table.setRowCount(len(lignes))
        row = 0
        for ligne in lignes:
            self.table.setItem(row, 0, QTableWidgetItem(str(ligne[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(ligne[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(ligne[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(ligne[3])))
            self.table.setItem(row, 4, QTableWidgetItem(str(ligne[4])))
            self.table.setItem(row, 5, QTableWidgetItem(str(ligne[5])))
            self.table.setItem(row, 6, QTableWidgetItem(str(ligne[6])))
            self.table.setItem(row, 7, QTableWidgetItem(str(ligne[7])))
            self.table.setItem(row, 8, QTableWidgetItem(str(ligne[8])))
            self.table.setItem(row, 9, QTableWidgetItem(str(ligne[9])))
            row += 1

    def loadDataUser(self):
        lignes = User().selectUserInfo()
        self.table.setRowCount(len(lignes))
        row = 0
        for ligne in lignes:
            self.table.setItem(row, 0, QTableWidgetItem(str(ligne[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(ligne[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(ligne[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(ligne[3])))
            self.table.setItem(row, 4, QTableWidgetItem(str(ligne[4])))
            self.table.setItem(row, 5, QTableWidgetItem(str(ligne[5])))
            self.table.setItem(row, 6, QTableWidgetItem(str(ligne[6])))
            self.table.setItem(row, 7, QTableWidgetItem(str(ligne[7])))
            self.table.setItem(row, 8, QTableWidgetItem(str(ligne[8])))
            self.table.setItem(row, 9, QTableWidgetItem(str(ligne[9])))
            self.table.setItem(row, 10, QTableWidgetItem(str(ligne[10])))
            self.table.setItem(row, 11, QTableWidgetItem(str(ligne[11])))
            row += 1

    def matchTableEvent(self):
        index = self.table.currentRow()
        row = Match().selectMatchById(self.table.item(index, 0).text())
        match_dialog = MatchDialog(self, str(row[0]), str(row[1]), str(row[2]),
                                   str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7]), str(row[8]),
                                   str(row[9])
                                   )
        result = match_dialog.exec_()
        if result == QDialog.Rejected:
            self.change_body_content()
            self.match_content()

    def userTableEvent(self):
        index = self.table.currentRow()
        row = User().select_userById(self.table.item(index, 0).text())
        compte_dialog = CompteDialog(self, str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]),
                                     str(row[6]), str(row[7]), str(row[8]), str(row[9]), str(row[10]), str(row[11])
                                     )
        result = compte_dialog.exec_()
        if result == QDialog.Rejected:
            self.change_body_content()
            self.compte_content()

    def add_data_pari(self, id_match, eq1, eq2, cote):
        # Vérifie si l'ID du match est déjà présent dans self.pari_data
        if not any(item['id'] == id_match for item in self.pari_data):
            # Ajout du pari à self.pari_data si l'ID du match n'est pas présent
            self.pari_data.append({'id': id_match, 'receiver_team': eq1, 'visitor_team': eq2, 'cote': cote})
            self.change_bet_info()
            self.bet_info_content()

    def somme_cote(self):
        cote_total = 0.00
        for i in range(len(self.pari_data)):
            cote_total += float(self.pari_data[i]['cote'])
        return cote_total

    def on_text_changed(self):
        if self.bet_amount_field.text() == '':
            self.somme_montant = float(0.00) * float(self.somme_cote())
            self.bet_win_value_lbl.setText(f"{self.somme_montant}")
        else:
                self.somme_montant = float(self.bet_amount_field.text()) * float(self.somme_cote())
                self.bet_win_value_lbl.setText(f"{self.somme_montant}")


    def placerPari(self):
        if self.pari_data == []:
            QMessageBox.about(self, 'Erreur', "Ajouter un ou des match pour pouvoir placeR votre pari")
        elif float(User().select_userById(User().display_UserAuth())[9]) < float(self.bet_amount_field.text()):
            QMessageBox.about(self, 'Erreur', "Vous n'avez pas assez d'argent pour cet action")
        elif float(self.bet_amount_field.text()) == 0.00 or float(self.bet_amount_field.text()) < 10.00 or float(self.bet_amount_field.text()) > 75000.00:
            QMessageBox.about(self, 'Erreur', f"Le montant de pariage est au minimum {10.00} Gourdes et au maximun 75000")
        else:
            code_pariage = self.generate_unique_id(5)
            account_id = User().display_UserAuth()
            match_id = self.filtrage_score_prevu()[1]
            bet_date = date.today()
            bet_amount = float(self.bet_amount_field.text())
            bet_score = self.filtrage_score_prevu()[0]
            equipe_choisies = self.filtrage_score_prevu()[3]
            cote = self.filtrage_score_prevu()[2]
            statut_pariage = []
            for i in range(len(match_id)):
                if Bet().insert(code_pariage, account_id, bet_date, bet_amount) == "add_success":
                    if Match().selectMatchById(match_id[i])[8] == bet_score[i]:
                        equipe_choisie = self.check_equipe_choisie(bet_score[i], equipe_choisies[i])
                        Bet().insert_mach_choisie(code_pariage, match_id[i], equipe_choisie, cote[i], bet_score[i],
                                                  "Gagne")
                        statut_pariage.append(1)
                    else:
                        equipe_choisie = self.check_equipe_choisie(bet_score[i], equipe_choisies[i])
                        Bet().insert_mach_choisie(code_pariage, match_id[i], equipe_choisie, cote[i], bet_score[i],
                                                  "Perdu")
                        statut_pariage.append(0)
            if 0 in statut_pariage:
                amount = float(User().select_userById(account_id)[9]) - float(bet_amount)
                RechargeAccount().updateBalance(account_id, amount)
                QMessageBox.about(self, 'perdu', f"Vous avez perdu une somme de {bet_amount} Gourdes")
                self.change_header()

            else:
                mnt_gagne=(float(bet_amount) * float(self.somme_cote()))
                amount = float(User().select_userById(account_id)[9]) + mnt_gagne
                RechargeAccount().updateBalance(account_id, amount)
                QMessageBox.about(self, 'gagne', f"Vous avez gagne une somme de {mnt_gagne} Gourdes")
                print(code_pariage)
                print(Payment().insert(code_pariage,bet_date,mnt_gagne))
                self.change_header()

    def filtrage_score_prevu(self):
        score = []
        pattern = r"^\d+:\d+$"
        for i in range(len(self.score_prevues)):
            if self.score_prevues is not None:
                score.append(self.score_prevues[i].text())

        if any(len(elem) == 0 for elem in score):
            QMessageBox.about(self, 'Erreur', "Remplissez tous les champs score prevus")
            return False
        elif not all(re.match(pattern, elem) for elem in score):
            QMessageBox.about(self, 'Erreur', "vous devez respecter le format : ex: 1: 0")
            return False
        else:
            return [score, self.id_match_choisi, self.cote_bet, self.rencontre]

    def delete_item_pari(self, pari_id):
        for i, element in list(enumerate(self.pari_data)):
            if element['id'] == pari_id:
                del self.pari_data[i]
                break
        else:
            print()
        self.change_bet_info()
        self.bet_info_content()

    def generate_unique_id(self, length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def check_equipe_choisie(self, score_prevu, rencontre):
        # Séparer les valeurs devant et derrière les deux points
        val1, val2 = score_prevu.split(':')
        # Convertir les valeurs en nombres entiers
        val1 = int(val1)
        val2 = int(val2)
        # Comparer les valeurs et renvoyer le résultat approprié
        if val1 > val2:
            return rencontre['receiver_team']
        elif val1 < val2:
            return rencontre['visitor_team']
        else:
            return "match nul"


if __name__ == '__main__':
    app = QApplication([])
    main = mainView()
    app.exec_()
