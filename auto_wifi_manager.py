import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *

import drive_found


class Ui(QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('auto_wifi_manager.ui', self)
        self.setFixedSize(self.size())
        self.show()

        self.combobox = self.findChild(QComboBox, "device_select")
        self.deviceSelectLabel = self.findChild(QLabel, "selected_device")
        self.refreshBtn = self.findChild(QPushButton, "refresh_btn")
        self.verifyBtn = self.findChild(QPushButton, "device_verification_btn")
        self.frame = self.findChild(QFrame, "frame")
        self.verifyStatus = self.findChild(QLabel, "verification_status")

        self.initialization()

    def initialization(self):
        self.combobox.addItem("Select the Device")
        self.combobox.addItems(drive_found.get_devices())
        self.update_device_select_label()
        self.combobox.currentIndexChanged.connect(self.update_device_select_label)
        self.refreshBtn.clicked.connect(self.refresh_device)
        self.verifyBtn.clicked.connect(lambda: self.verify_device(self.combobox.currentText()))
        self.frame.setEnabled(False)
        self.verifyStatus.setText("")

    def verify_device(self, directory):
        if os.path.isdir(directory + "/home/pi/"):
            self.frame.setEnabled(True)
            self.verifyStatus.setText("<html><head/><body><p><span style='color:#177B0A;'>Device is "
                                      "Okay</span></p></body></html>")
        else:
            self.frame.setEnabled(False)
            self.verifyStatus.setText("<html><head/><body><p><span style='color:#ff0000;'>Device Verification Failed, "
                                      "Select the correct device</span></p></body></html>")

    def refresh_device(self):
        self.combobox.clear()
        self.combobox.addItem("Select the Device")
        self.combobox.addItems(drive_found.get_devices())
        self.update_device_select_label()
        self.combobox.currentIndexChanged.connect(self.update_device_select_label)
        self.verifyStatus.setText("")
        self.frame.setEnabled(False)

    def update_device_select_label(self):
        if self.combobox.currentIndex() == 0:
            self.deviceSelectLabel.setText("")
            self.verifyBtn.setEnabled(False)
        else:
            self.deviceSelectLabel.setText(self.combobox.currentText())
            self.verifyBtn.setEnabled(True)

        self.frame.setEnabled(False)
        self.verifyStatus.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
