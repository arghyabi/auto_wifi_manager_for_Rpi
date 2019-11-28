import os
import sys
import re

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import drive_found


class Ui(QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('auto_wifi_manager.ui', self)
        self.wifiWidget = uic.loadUi('auto_wifi_manager_wifi_credential.ui')
        self.setFixedSize(self.size())
        self.show()

        self.combobox = self.findChild(QComboBox, "device_select")
        self.deviceSelectLabel = self.findChild(QLabel, "selected_device")
        self.refreshBtn = self.findChild(QPushButton, "refresh_btn")
        self.verifyBtn = self.findChild(QPushButton, "device_verification_btn")
        self.frame = self.findChild(QFrame, "frame")
        self.verifyStatus = self.findChild(QLabel, "verification_status")
        self.wifi_credential = self.findChild(QCheckBox, "wifi_credential_checkBox")
        self.ip_founder_checkBox = self.findChild(QCheckBox, "ip_founder_checkBox")
        self.final_status_label = self.findChild(QLabel, "final_status_label")

        self.wifi_list_combo = self.wifiWidget.findChild(QComboBox, "wifiListCombo")
        self.wifi_ssid = self.wifiWidget.findChild(QLineEdit, "wifi_ssid")
        self.wifi_psk = self.wifiWidget.findChild(QLineEdit, "wifi_psk")
        self.wifi_Edit = self.wifiWidget.findChild(QPushButton, "wifi_Edit")
        self.wifi_Edit_cancel = self.wifiWidget.findChild(QPushButton, "wifiEditCancel")
        self.wifi_Del = self.wifiWidget.findChild(QPushButton, "wifi_Del")
        self.wifi_status = self.wifiWidget.findChild(QLabel, "status_label")
        self.availableWiFiradio = self.wifiWidget.findChild(QRadioButton, "availableWiFiradio")
        self.addNewWifiradio = self.wifiWidget.findChild(QRadioButton, "addNewWifiradio")
        self.diaglog_btn = self.wifiWidget.findChild(QDialogButtonBox, "diaglog_box")

        self.wifi_path = ""

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
        self.wifi_credential.stateChanged.connect(self.add_modify_wifi_credential)
        self.ip_founder_checkBox.stateChanged.connect(self.ip_founder)

        self.wifi_list_combo.addItem("Select WiFi")
        self.wifi_list_combo.currentIndexChanged.connect(self.wifi_select_change)
        self.wifi_Edit.clicked.connect(self.wifi_edit_btn_callback)
        self.wifi_Del.clicked.connect(self.wifi_del_btn_callback)
        self.wifi_psk.setEnabled(False)
        self.wifi_ssid.setEnabled(False)
        self.wifi_Edit.setEnabled(False)
        self.wifi_Edit_cancel.hide()
        self.wifi_Edit_cancel.clicked.connect(self.wifi_edit_cancel_btn_callback)
        self.wifi_Del.setEnabled(False)
        self.wifi_status.setText("")
        self.diaglog_btn.clicked.connect(lambda: self.dialog_btn_callback())

        self.wifiWidget.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.wifiWidget.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

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

    def add_modify_wifi_credential(self):
        if self.wifi_credential.isChecked():
            self.setEnabled(False)
            self.wifiWidget.show()
            wifi_list = []
            self.wifi_path = self.combobox.currentText() + "/etc/wpa_supplicant/wpa_supplicant.conf"

            if os.path.isfile(self.wifi_path):
                f = open(self.wifi_path, "r")
                data = [line.strip() for line in f.read().split("\n") if line.split()]
                f.close()

                for line in range(len(data)):
                    if re.findall("^network", data[line]) and re.findall("^ssid", data[line+1]):
                        wifi_list.append(data[line+1][6:-1])
                self.wifi_list_combo.clear()
                self.wifi_list_combo.addItem("Select WiFi")
                self.wifi_list_combo.addItems(wifi_list)
            else:
                self.final_status_label.setText("<html><head/><body><p><span style='color:#ff0000;'>Wifi credential "
                                                "file not found...</span></p></body></html>")
        else:
            self.final_status_label.setText("")

    def dialog_btn_callback(self):
        self.wifiWidget.hide()
        self.setEnabled(True)

    def ip_founder(self):
        pass

    def wifi_select_change(self):
        if self.wifi_list_combo.currentIndex != 0:
            self.wifi_ssid.setText(self.wifi_list_combo.currentText())
            self.wifi_ssid.setEnabled(True)
            self.wifi_Edit.setEnabled(True)
            self.wifi_Del.setEnabled(True)
        else:
            self.wifi_ssid.setText('')
            self.wifi_ssid.setEnabled(False)
            self.wifi_Edit.setEnabled(False)
            self.wifi_Del.setEnabled(False)

    def wifi_edit_btn_callback(self):
        if self.wifi_Edit.text() == "Edit":
            self.wifi_psk.setEnabled(True)
            self.wifi_list_combo.setEnabled(False)
            self.availableWiFiradio.setEnabled(False)
            self.addNewWifiradio.setEnabled(False)
            self.wifi_Del.setEnabled(False)
            self.wifi_Edit.setText("OK")
            self.wifi_Edit_cancel.show()
        else:
            self.wifi_Edit.setText("Edit")
            if self.wifi_update():
                self.wifi_list_combo.setEnabled(True)
                self.availableWiFiradio.setEnabled(True)
                self.addNewWifiradio.setEnabled(True)
                self.wifi_Del.setEnabled(True)
                self.wifi_psk.setEnabled(False)
                self.wifi_psk.setText("")
                self.wifi_status.setText("<html><head/><body><p><span style='color:#177B0A;'>Wifi details updated."
                                            "</span></p></body></html>")
                self.wifi_Edit_cancel.hide()

    def wifi_edit_cancel_btn_callback(self):
        self.wifi_psk.setEnabled(False)
        self.wifi_list_combo.setEnabled(True)
        self.availableWiFiradio.setEnabled(True)
        self.addNewWifiradio.setEnabled(True)
        self.wifi_Del.setEnabled(True)
        self.wifi_Edit.setText("Edit")
        self.wifi_Edit_cancel.hide()

    def wifi_update(self):
        if os.path.isfile(self.wifi_path):
            f = open(self.wifi_path, "r")
            data = [line.strip() for line in f.read().split("\n") if line.split()]
            f.close()

            for line in range(len(data)):
                if re.findall('^ssid="' + self.wifi_ssid.text() + '"', data[line]):
                    data[line+1] = 'psk="' + str(self.wifi_psk.text()) + '"'
            
            temp = ""
            for line in data:
                temp += str(line) + "\n"
            f = open(self.wifi_path, "w")
            f.write(temp)
            f.close()
            return True
        else:
            self.wifi_status.setText("<html><head/><body><p><span style='color:#ff0000;'>Wifi credential file "
                                            "not found...</span></p></body></html>")
            return False

    def wifi_del_btn_callback(self):
        if os.path.isfile(self.wifi_path):
            f = open(self.wifi_path, "r")
            data = [line.strip() for line in f.read().split("\n") if line.split()]
            f.close()

            inNet = False
            inNetLine = []
            match = False

            for line in range(len(data)):
                if inNet:
                    if re.findall('^}', data[line]):
                        if match:
                            inNetLine.append(line)
                            for j in range(len(inNetLine)-1):
                                data.pop(inNetLine[1])
                            inNet = False
                            inNetLine = []
                            match = False
                            break
                        else:
                            inNet = False
                            inNetLine = []
                    if re.findall('^ssid="' + self.wifi_ssid.text() + '"', data[line]):
                        match = True
                        inNetLine.append(line)
                    inNetLine.append(line)
                else:
                    if re.findall('^network={', data[line]):
                        inNet = True
                        inNetLine.append(line)
            
            temp = ""
            for line in data:
                temp += str(line) + "\n"
            f = open(self.wifi_path, "w")
            f.write(temp)
            f.close()
            self.add_modify_wifi_credential()
            self.wifi_status.setText("<html><head/><body><p><span style='color:#177B0A;'>Wifi details deleted."
                                            "</span></p></body></html>")
            return True
        else:
            self.wifi_status.setText("<html><head/><body><p><span style='color:#ff0000;'>Wifi credential file "
                                            "not found...</span></p></body></html>")
            return False


if __name__ == '__main__':
    if os.getuid() != 0:
        print("Permission Denied\nRun as Super User")
        exit(0)
    else:
        app = QApplication(sys.argv)
        window = Ui()
        sys.exit(app.exec_())
