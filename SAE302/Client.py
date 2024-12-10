import sys
import socket
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt

class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client - Envoi de code Python")
        
        self.server_ip = QLineEdit("127.0.0.1")
        self.server_port = QLineEdit("5000")
        self.code_edit = QTextEdit()
        self.code_edit.setPlainText("print('Hello from the client GUI')")
        
        self.load_file_button = QPushButton("Charger un fichier")
        self.load_file_button.clicked.connect(self.load_file)
        
        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_code)
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        
        # Layout
        layout = QVBoxLayout()
        
        # Zone pour l'IP et le port
        server_layout = QHBoxLayout()
        server_layout.addWidget(QLabel("IP Serveur:"))
        server_layout.addWidget(self.server_ip)
        server_layout.addWidget(QLabel("Port:"))
        server_layout.addWidget(self.server_port)
        
        layout.addLayout(server_layout)
        
        # Zone pour le code et les boutons
        layout.addWidget(QLabel("Code Python:"))
        layout.addWidget(self.code_edit)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_file_button)
        button_layout.addWidget(self.send_button)
        layout.addLayout(button_layout)
        
        layout.addWidget(QLabel("Résultat:"))
        layout.addWidget(self.result_display)
        
        self.setLayout(layout)
        
    def load_file(self):
        """Ouvre une boîte de dialogue pour sélectionner un fichier Python, et charge son contenu dans la zone de texte."""
        file_dialog = QFileDialog(self, "Sélectionner un fichier Python")
        file_dialog.setNameFilter("Fichiers Python (*.py)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                    self.code_edit.setPlainText(code_content)
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier : {e}")
        
    def send_code(self):
        ip = self.server_ip.text().strip()
        port_str = self.server_port.text().strip()
        
        if not port_str.isdigit():
            QMessageBox.critical(self, "Erreur", "Le port doit être un nombre.")
            return
        port = int(port_str)
        
        code_str = self.code_edit.toPlainText()
        if not code_str:
            QMessageBox.warning(self, "Attention", "Le code est vide.")
            return
        
        # Envoi du code au serveur maître
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                code_bytes = code_str.encode('utf-8')
                size = len(code_bytes)
                s.sendall(size.to_bytes(4, 'big'))
                s.sendall(code_bytes)

                # Réception du résultat
                resp_size_data = s.recv(4)
                if len(resp_size_data) < 4:
                    self.result_display.setPlainText("Erreur de réception (taille de la réponse)")
                    return
                resp_size = int.from_bytes(resp_size_data, 'big')
                
                response = b''
                while len(response) < resp_size:
                    chunk = s.recv(resp_size - len(response))
                    if not chunk:
                        break
                    response += chunk
                self.result_display.setPlainText(response.decode('utf-8'))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de contacter le serveur: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ClientGUI()
    gui.show()
    sys.exit(app.exec())
