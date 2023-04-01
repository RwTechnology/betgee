import mysql.connector
from PyQt5.QtWidgets import QMessageBox

class DBConnection:

    def connection(self):
        try:
            self.conn=mysql.connector.connect(host='localhost',database='geebet',user='root',password='root')
        except mysql.connector.Error as erreur:
            QMessageBox.warning(None, "Erreur de connexion", "Impossible de se connecter a la BD" + str(erreur),QMessageBox.Ok)
        return self.conn