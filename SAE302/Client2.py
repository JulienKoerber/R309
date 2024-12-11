import sys
import socket

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QFileDialog,
    QGroupBox, QMenuBar, QMenu, QFrame, QComboBox
)
from PyQt6.QtGui import QAction, QFont, QPalette, QColor
from PyQt6.QtCore import Qt

class ClientGUI2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client 2 - Exécution de code Python/Java")
        
        self.setMinimumSize(600, 400)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        self.setPalette(palette)
        
        title_font = QFont("Arial", 12, QFont.Weight.Bold)
        
        menubar = QMenuBar(self)
        file_menu = QMenu("Fichier", self)
        
        load_action = QAction("Charger un fichier", self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)

        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close_application)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)
        
        menubar.addMenu(file_menu)
        
        button_style = """
            QPushButton {
                color: #ffffff; 
                background-color: #007ACC; 
                border: none; 
                padding: 8px 15px; 
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """
        
        lineedit_style = """
            QLineEdit {
                color: #ffffff;
                background-color: #007ACC;
                border: none;
                padding: 4px 8px;
                font-weight: bold;
                border-radius: 4px;
            }
        """
        
        label_style = """
            QLabel {
                font-weight: bold;
                color: #005A9E;
            }
        """

        groupbox_style = """
            QGroupBox {
                color: #000000; 
                font-weight: bold;
            }
        """
        
        server_group = QGroupBox("Paramètres du serveur")
        server_group.setFont(title_font)
        server_group.setStyleSheet(groupbox_style)
        
        self.server_ip = QLineEdit("127.0.0.1")
        self.server_ip.setStyleSheet(lineedit_style)
        
        self.server_port = QLineEdit("5000")
        self.server_port.setStyleSheet(lineedit_style)

        ip_label = QLabel("IP :")
        ip_label.setStyleSheet(label_style)
        port_label = QLabel("Port :")
        port_label.setStyleSheet(label_style)
        
        server_layout = QHBoxLayout()
        server_layout.addWidget(ip_label)
        server_layout.addWidget(self.server_ip)
        server_layout.addWidget(port_label)
        server_layout.addWidget(self.server_port)
        
        server_group.setLayout(server_layout)
        
        code_group = QGroupBox("Code")
        code_group.setFont(title_font)
        code_group.setStyleSheet(groupbox_style)
        
        self.code_edit = QTextEdit()
        self.code_edit.setPlainText("print('Hello from Client 2')")
        self.code_edit.setStyleSheet("QTextEdit { color: #000000; background-color: #ffffff; }")

        self.load_file_button = QPushButton("Charger un fichier")
        self.load_file_button.clicked.connect(self.load_file)
        self.load_file_button.setStyleSheet(button_style)
        
        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_code)
        self.send_button.setStyleSheet(button_style)
        
        self.clear_button = QPushButton("Effacer")
        self.clear_button.clicked.connect(self.clear_code)
        self.clear_button.setStyleSheet(button_style)
        
        self.quit_button = QPushButton("Quitter")
        self.quit_button.clicked.connect(self.close_application)
        self.quit_button.setStyleSheet(button_style)
        
        language_label = QLabel("Langage :")
        language_label.setStyleSheet(label_style)
        self.language_combo = QComboBox()
        self.language_combo.addItem("Python")
        self.language_combo.addItem("Java")
        
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(language_label)
        lang_layout.addWidget(self.language_combo)
        
        code_button_layout = QHBoxLayout()
        code_button_layout.addWidget(self.load_file_button)
        code_button_layout.addWidget(self.send_button)
        code_button_layout.addWidget(self.clear_button)
        code_button_layout.addWidget(self.quit_button)
        
        code_layout = QVBoxLayout()
        code_layout.addLayout(lang_layout)
        code_layout.addWidget(self.code_edit)
        code_layout.addLayout(code_button_layout)
        
        code_group.setLayout(code_layout)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)

        result_group = QGroupBox("Résultat")
        result_group.setFont(title_font)
        result_group.setStyleSheet(groupbox_style)
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("QTextEdit { color: #000000; background-color: #ffffff; }")
        
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.result_display)
        result_group.setLayout(result_layout)
        
        main_layout = QVBoxLayout()
        main_layout.setMenuBar(menubar)
        main_layout.addWidget(server_group)
        main_layout.addWidget(code_group)
        main_layout.addWidget(line)
        main_layout.addWidget(result_group)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        self.setLayout(main_layout)
        
    def load_file(self):
        file_dialog = QFileDialog(self, "Sélectionner un fichier")
        file_dialog.setNameFilter("Fichiers Python/Java (*.py *.java)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                    self.code_edit.setPlainText(code_content)
                    if file_path.endswith(".py"):
                        self.language_combo.setCurrentText("Python")
                    elif file_path.endswith(".java"):
                        self.language_combo.setCurrentText("Java")
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier : {e}")
    
    def clear_code(self):
        self.code_edit.clear()
    
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
        
        language = self.language_combo.currentText().lower()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                lang_bytes = language.encode('utf-8')
                lang_size = len(lang_bytes)
                s.sendall(lang_size.to_bytes(4, 'big'))
                s.sendall(lang_bytes)
                
                code_bytes = code_str.encode('utf-8')
                size = len(code_bytes)
                s.sendall(size.to_bytes(4, 'big'))
                s.sendall(code_bytes)

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

    def close_application(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui2 = ClientGUI2()
    gui2.show()
    sys.exit(app.exec())
