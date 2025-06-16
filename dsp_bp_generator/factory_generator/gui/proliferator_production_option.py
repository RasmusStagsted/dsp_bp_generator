from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox

class ProliferatorProductionOption(QWidget):
    def __init__(self, update_callback = None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.label = QLabel("Choose if the proliferator should be produced internally or externally:")
        self.layout.addWidget(self.label)
        self.layout_mki = QHBoxLayout()
        self.layout_mkii = QHBoxLayout()
        self.layout_mkiii = QHBoxLayout()
        self.layout.addLayout(self.layout_mki)
        self.layout.addLayout(self.layout_mkii)
        self.layout.addLayout(self.layout_mkiii)
        self.mki_label = QLabel("Proliferator MK.I production:")
        self.mki = QComboBox()
        self.mki.addItems(["Unused"])
        self.layout_mki.addWidget(self.mki_label)
        self.layout_mki.addWidget(self.mki)

        self.mkii_label = QLabel("Proliferator MK.II production:")
        self.mkii = QComboBox()
        self.mkii.addItems(["Unused"])
        self.layout_mkii.addWidget(self.mkii_label)
        self.layout_mkii.addWidget(self.mkii)

        self.mkiii_label = QLabel("Proliferator MK.III production:")
        self.mkiii = QComboBox()
        self.mkiii.addItems(["Unused"])
        self.layout_mkiii.addWidget(self.mkiii_label)
        self.layout_mkiii.addWidget(self.mkiii)

        if update_callback != None:
            self.mki.currentTextChanged.connect(lambda: update_callback("MK.I"))
            self.mkii.currentTextChanged.connect(lambda: update_callback("MK.II"))
            self.mkiii.currentTextChanged.connect(lambda: update_callback("MK.III"))

        self.setLayout(self.layout)
    
    def update(self, proliferators, index):
        proliferators = [proliferators[i].currentText() for i in range(len(proliferators))]
        proliferators = list(set(proliferators))
        proliferators.sort()
        if "None" in proliferators:
            proliferators.remove("None")
        boxes = {
            "MK.I": self.mki,
            "MK.II": self.mkii,
            "MK.III": self.mkiii
        }
        for key, box in boxes.items():
            if key in proliferators:
                ProliferatorProductionOption.set_options(box, ["Internal", "External"])
            else:
                ProliferatorProductionOption.set_options(box, ["Unused"])
                
    @staticmethod
    def set_options(combo_box, options):
        current_value = combo_box.currentText()
        combo_box.clear()
        combo_box.addItems(options)
        if current_value in options:
            combo_box.setCurrentText(current_value)
        else:
            combo_box.setCurrentIndex(0)
    
    def get_proliferator_assembly(self):
        return {
            "MK.I": self.mki.currentText(),
            "MK.II": self.mkii.currentText(),
            "MK.III": self.mkiii.currentText()
        }