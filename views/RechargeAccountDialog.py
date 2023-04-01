from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, \
    QLineEdit, QComboBox, QDateEdit, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate

from controllers.RechargeAccountController import RechargeAccountController


class RechargeAccountDialog(QDialog):
    def __init__(self, parent):
        super(RechargeAccountDialog, self).__init__(parent)
        self.setFixedSize(300, 300)
        self.setStyleSheet(open("../assets/css/style.css", "r").read())
        self.setWindowTitle(" Ajout de credit | GeeBet")
        self.center()
        self.mainLayout = QVBoxLayout()
        self.initUI()


    def initUI(self):
        self.groupBox = QGroupBox()
        self.groupBox.setFixedSize(250, 250)
        self.groupBox.setObjectName("grpbx")

        self.Vbox = QVBoxLayout()
        self.verticalLayout = QVBoxLayout()
        self.Hbox = QHBoxLayout()


        #Code du pariage
        self.codeLabel = QLabel('Code Parieur')
        self.codeField=QLineEdit()
        self.codeField.setObjectName("fields")
        self.codeField.setStyleSheet(self.styleSheet())


        # Champ montant
        self.amountLabel = QLabel('Montant')
        self.amountField = QLineEdit()
        self.amountField.setObjectName("fields")
        self.amountField.setStyleSheet(self.styleSheet())
        self.amountField.setTextMargins(3, 0, 3, 0)
        self.amountField.setMinimumWidth(200)
        self.amountField.setMaximumWidth(300)

        # Ajout des colonnes dans le add formlayout
        self.Vbox.addWidget(self.codeLabel)
        self.Vbox.addWidget(self.codeField)
        self.Hbox.addLayout(self.Vbox)

        self.Vbox.addWidget(self.amountLabel)
        self.Vbox.addWidget(self.amountField)
        self.Hbox.addLayout(self.Vbox)

        self.verticalLayout.addLayout(self.Hbox)
        self.verticalLayout.setAlignment(Qt.AlignCenter)
        self.verticalLayout.setContentsMargins(10, 0, 10, 0)


        self.save_credit_button = QPushButton("Enregistrer", self)
        self.save_credit_button.setObjectName("btn_primary")
        self.save_credit_button.setStyleSheet(self.styleSheet())

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(Qt.AlignCenter)


        self.horizontalLayout.addWidget(self.save_credit_button)


        self.groupBox.setLayout(self.verticalLayout)
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.show()
        self.mainLayout.addWidget(self.groupBox)

        self.mainLayout.setAlignment(Qt.AlignCenter)

        self.groupBox.setLayout(self.verticalLayout)


        self.groupBox.setLayout(self.verticalLayout)
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.show()
        self.mainLayout.addWidget(self.groupBox)

        self.mainLayout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.mainLayout)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Les evenements
        self.save_credit_button.clicked.connect(self.recharge)




    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def recharge(self):
        current_date = QDate.currentDate()

        response = RechargeAccountController().add_credit(
            self.codeField.text(),
            self.amountField.text(),
            current_date.toPyDate()
        )
        if response == 'add_success':
            self.close()
            QMessageBox.about(self, 'Informations', "Credit ajoute")
        else:
            QMessageBox.about(self, 'Erreur', response)
