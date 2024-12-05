import sys
import socket
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QTextEdit, QMessageBox

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Layout principal
        self.layout = QVBoxLayout()

        # IP et Port
        self.ip_entry = QLineEdit(self)
        self.ip_entry.setPlaceholderText('IP du Serveur')
        self.layout.addWidget(self.ip_entry)

        self.port_entry = QLineEdit(self)
        self.port_entry.setPlaceholderText('Port du Serveur')
        self.layout.addWidget(self.port_entry)

        # Sélection du fichier
        self.file_button = QPushButton("Choisir un fichier", self)
        self.file_button.clicked.connect(self.choose_file)
        self.layout.addWidget(self.file_button)

        # Affichage du fichier sélectionné
        self.file_display = QLineEdit(self)
        self.layout.addWidget(self.file_display)

        # Zone de texte pour afficher le résultat de l'exécution
        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText("Résultat d'exécution...")
        self.layout.addWidget(self.output_text)

        # Bouton pour envoyer le fichier
        self.execute_button = QPushButton("Exécuter le fichier", self)
        self.execute_button.clicked.connect(self.execute_file)
        self.layout.addWidget(self.execute_button)

        # Bouton de connexion
        self.connect_button = QPushButton("Se connecter au serveur", self)
        self.connect_button.clicked.connect(self.connect_to_server)
        self.layout.addWidget(self.connect_button)

        # Bouton pour fermer le client
        self.shutdown_button = QPushButton("Fermer le client", self)
        self.shutdown_button.clicked.connect(self.shutdown_client)
        self.layout.addWidget(self.shutdown_button)

        # Initialiser la fenêtre
        self.setLayout(self.layout)
        self.setWindowTitle('Client Python')
        self.show()

    def choose_file(self):
        # Ouvrir la boîte de dialogue pour choisir un fichier Python
        file_path, _ = QFileDialog.getOpenFileName(self, 'Choisir un fichier Python', '', 'Python Files (*.py)')
        if file_path:
            self.file_display.setText(file_path)

    def connect_to_server(self):
        # Connexion au serveur
        server_ip = self.ip_entry.text()
        server_port = self.port_entry.text()

        if not server_ip or not server_port:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une adresse IP et un port valides.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, int(server_port)))
            QMessageBox.information(self, "Connexion réussie", "Connexion réussie au serveur.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur de connexion", f"Erreur de connexion : {e}")

    def execute_file(self):
        # Fonction pour envoyer le fichier et exécuter le code Python
        file_path = self.file_display.text()

        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un fichier valide.")
            return

        if not file_path.endswith('.py'):
            QMessageBox.warning(self, "Erreur", "Seuls les fichiers .py sont acceptés.")
            return

        # Lancer l'exécution du fichier dans un thread séparé
        threading.Thread(target=self.send_and_execute_file, args=(file_path,), daemon=True).start()

    def send_and_execute_file(self, file_path):
        try:
            # Envoyer le fichier au serveur
            filename = os.path.basename(file_path)

            # Envoyer le nom du fichier au serveur
            self.client_socket.sendall(filename.encode('utf-8'))

            # Envoyer le contenu du fichier
            with open(file_path, 'rb') as file:
                while chunk := file.read(4096):
                    self.client_socket.sendall(chunk)

            # Attendre la réponse du serveur
            result = self.client_socket.recv(4096).decode('utf-8')

            # Afficher le résultat dans la zone de texte
            self.output_text.append(result)

        except Exception as e:
            self.output_text.append(f"Erreur lors de l'envoi ou de l'exécution du fichier : {e}")

    def shutdown_client(self):
        # Demander confirmation avant de fermer l'application
        reply = QMessageBox.question(self, 'Fermer le client', 'Voulez-vous vraiment fermer le client ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Réinitialiser les champs IP et port
            self.ip_entry.clear()
            self.port_entry.clear()

            # Fermer l'application
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_app = ClientApp()
    sys.exit(app.exec_())
