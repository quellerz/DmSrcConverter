import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QRadioButton
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QIcon

class main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Valve Hammer Unit Conventer')
        self.setWindowIcon(QIcon('icon.ico'))
        self.setFixedSize(300, 170)

        self.input_value = QLineEdit()
        self.input_value.setPlaceholderText('Enter value')

        self.input_unit = QComboBox()
        self.output_unit = QComboBox()

        self.units = ['meters', 'kilometers', 'centimeters', 'millimeters', 'miles', 'feet', 'inches', 'yards', 'units', 'skybox']
        self.input_unit.addItems(self.units)
        self.output_unit.addItems(self.units)

        self.result_value = QLineEdit()
        self.result_value.setPlaceholderText('Result')
        self.result_value.setReadOnly(True)

        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert)

        self.architecture_radio = QRadioButton('Architecture Metrics')
        self.entity_radio = QRadioButton('Entity Metrics')
        self.architecture_radio.setChecked(True)

        self.link_label = QLabel()
        self.link_label.setText('<a href="https://developer.valvesoftware.com/wiki/Dimensions_(Half-Life_2_and_Counter-Strike:_Source)">' 'Official Source Engine dimensions guide</a>')
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        unit_layout = QHBoxLayout()
        radio_layout = QHBoxLayout()
        result_layout = QHBoxLayout()
        link_layout = QHBoxLayout()

        input_layout.addWidget(QLabel('Value:'))
        input_layout.addWidget(self.input_value)

        unit_layout.addWidget(QLabel('From:'))
        unit_layout.addWidget(self.input_unit)
        unit_layout.addWidget(QLabel('To:'))
        unit_layout.addWidget(self.output_unit)

        radio_layout.addWidget(self.architecture_radio)
        radio_layout.addWidget(self.entity_radio)

        result_layout.addWidget(QLabel('Result:'))
        result_layout.addWidget(self.result_value)

        link_layout.addWidget(self.link_label)

        layout.addLayout(input_layout)
        layout.addLayout(unit_layout)
        layout.addLayout(radio_layout)
        layout.addWidget(self.convert_button)
        layout.addLayout(result_layout)
        layout.addLayout(link_layout)

        self.setLayout(layout)

        self.conversion_factors = { # based on a meter
            'meters': 1,
            'kilometers': 1000,
            'centimeters': 0.01,
            'millimeters': 0.001,
            'miles': 1609.34,
            'feet': 0.3048,
            'inches': 0.0254,
            'yards': 0.9144,
            'units': None,  # handeled in lines 92-95
            'skybox': 0.4064
        }

    def convert(self):
        try:
            value = float(self.input_value.text())
            from_unit = self.input_unit.currentText()
            to_unit = self.output_unit.currentText()

            factors = self.conversion_factors.copy()

            if self.architecture_radio.isChecked():
                factors['units'] = 0.3048 / 16
            elif self.entity_radio.isChecked():
                factors['units'] = 0.3048 / 12

            base_value = value * factors[from_unit]
            converted_value = base_value / factors[to_unit]

            rounded_value = round(converted_value, 2)

            self.result_value.setText(str(rounded_value))

        except ValueError:
            QMessageBox.critical(self, 'Error', 'Please enter a valid value')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 12px;
        }
    ''')
    window = main()
    window.show()
    sys.exit(app.exec())