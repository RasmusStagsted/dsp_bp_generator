from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

class BlueprintStringWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(QLabel("Blueprint string:"))
        self.generator_button = QPushButton("Generate blueprint!")
        self.layout.addWidget(self.generator_button)
        self.blueprint = QLineEdit()
        self.layout.addWidget(self.blueprint)
        self.copy = QPushButton("Copy blueprint!")
        self.copy.clicked.connect(self.copy_blueprint)
        self.layout.addWidget(self.copy)
        self.setLayout(self.layout)
        
    def set_callbacks(self, generate_blueprint_callback = None):
        self.generator_button.clicked.connect(generate_blueprint_callback)

    def copy_blueprint(self):
        try:
            import pyperclip
            pyperclip.copy(self.blueprint.text())
        except ImportError:
            print("pyperclip not installed, clipboard copy skipped.")
            print("Blueprint string:")
            print(self.blueprint.text())

    def set_blueprint_string(self, bp_string):
        self.blueprint.setText(bp_string)