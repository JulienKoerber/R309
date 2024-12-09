import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QProgressBar,
)
import socket
import os
import threading


class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client Python avec PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Initialisation du socket client
        self.client_socket = None

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Créer les sections de l'interface
        self.init_connection_section()
        self.init_file_section()
        self.init_result_section()

        # Bouton pour quitter l'application
        self.quit_button = QPushButton("Quitter")
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

    def init_connection_section(self):
        """Crée la section pour la connexion au serveur."""
        connection_group = QGroupBox("Connexion au serveur")
        connection_layout = QHBoxLayout()

        self.ip_label = QLabel("IP du Serveur :")
        self.ip_entry = QLineEdit()
        self.ip_entry.setText("127.0.0.1")

        self.port_label = QLabel("Port du Serveur :")
        self.port_entry = QLineEdit()
        self.port_entry.setText("5555")

        self.connect_button = QPushButton("Se Connecter")
        self.connect_button.clicked.connect(self.connect_to_server)

        connection_layout.addWidget(self.ip_label)
        connection_layout.addWidget(self.ip_entry)
        connection_layout.addWidget(self.port_label)
        connection_layout.addWidget(self.port_entry)
        connection_layout.addWidget(self.connect_button)

        connection_group.setLayout(connection_layout)
        self.layout.addWidget(connection_group)

    def init_file_section(self):
        """Crée la section pour sélectionner et envoyer un fichier."""
        file_group = QGroupBox("Envoi de fichier Python")
        file_layout = QVBoxLayout()

        self.file_button = QPushButton("Choisir un Fichier")
        self.file_button.clicked.connect(self.choose_file)
        self.file_button.setEnabled(False)

        self.file_path_label = QLabel("Aucun fichier sélectionné")
        self.file_path_label.setWordWrap(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.send_button = QPushButton("Envoyer et Exécuter")
        self.send_button.clicked.connect(self.send_and_execute_file)
        self.send_button.setEnabled(False)

        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.progress_bar)
        file_layout.addWidget(self.send_button)

        file_group.setLayout(file_layout)
        self.layout.addWidget(file_group)

    def init_result_section(self):
        """Crée la section pour afficher les résultats."""
        result_group = QGroupBox("Résultats de l'exécution")
        result_layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        result_layout.addWidget(self.result_text)
        result_group.setLayout(result_layout)
        self.layout.addWidget(result_group)

    def connect_to_server(self):
        """Se connecte au serveur avec l'IP et le port spécifiés."""
        server_ip = self.ip_entry.text()
        server_port = int(self.port_entry.text())

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, server_port))
            QMessageBox.information(self, "Succès", f"Connecté au serveur {server_ip}:{server_port}")
            self.file_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de se connecter au serveur : {e}")

    def choose_file(self):
        """Permet de sélectionner un fichier .py."""
        file_dialog = QFileDialog(self)
        self.file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier Python", "", "Python Files (*.py)")
        if self.file_path:
            self.file_path_label.setText(self.file_path)
            self.send_button.setEnabled(True)
        else:
            self.file_path_label.setText("Aucun fichier sélectionné")
            self.send_button.setEnabled(False)

    def send_and_execute_file(self):
        """Envoie le fichier au serveur pour exécution."""
        if not self.file_path or not os.path.exists(self.file_path):
            QMessageBox.critical(self, "Erreur", "Veuillez sélectionner un fichier valide.")
            return

        try:
            filename = os.path.basename(self.file_path)
            self.client_socket.sendall(filename.encode('utf-8'))

            with open(self.file_path, 'rb') as file:
                while chunk := file.read(4096):
                    self.client_socket.sendall(chunk)

            self.client_socket.sendall(b"END")

            data = b""
            while True:
                part = self.client_socket.recv(4096)
                if not part:
                    break
                data += part

            result = data.decode('utf-8')
            self.result_text.setPlainText(result)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

    def closeEvent(self, event):
        """Fermeture propre de la connexion lors de la fermeture de l'application."""
        if self.client_socket:
            self.client_socket.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ClientApp()
    client.show()
    sys.exit(app.exec_())
