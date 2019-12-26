import os
import sys
import re
import time

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import drive_found


class Ui(QDialog):
	def __init__(self):
		super(Ui, self).__init__()
		self.src_path = "/usr/share/auto_wifi_manager/"
		self.mainWidget = uic.loadUi(os.path.join(self.src_path + 'auto_wifi_manager.ui'))
		self.wifiWidget = uic.loadUi(os.path.join(self.src_path + 'auto_wifi_manager_wifi_credential.ui'))
		self.mainWidget.setFixedSize(self.mainWidget.size())
		self.wifiWidget.setFixedSize(self.wifiWidget.size())
		self.wifiWidget.move(QDesktopWidget().availableGeometry().center())
		self.mainWidget.show()

		self.combobox = self.mainWidget.findChild(QComboBox, "device_select")
		self.deviceSelectLabel = self.mainWidget.findChild(QLabel, "selected_device")
		self.refreshBtn = self.mainWidget.findChild(QPushButton, "refresh_btn")
		self.verifyBtn = self.mainWidget.findChild(QPushButton, "device_verification_btn")
		self.verifyStatus = self.mainWidget.findChild(QLabel, "verification_status")
		self.deviceModifyBtn = self.mainWidget.findChild(QPushButton, "device_modify_btn")

		self.tabWidget = self.wifiWidget.findChild(QTabWidget, "tabWidget")

		self.saved_wifi_combo_box = self.wifiWidget.findChild(QComboBox, "saved_wifi_combo_box")
		self.saved_wifi_ssid_textedit = self.wifiWidget.findChild(QLineEdit, "saved_wifi_ssid_textedit")
		self.saved_wifi_psk_textedit = self.wifiWidget.findChild(QLineEdit, "saved_wifi_psk_textedit")
		self.saved_wifi_edit_btn = self.wifiWidget.findChild(QPushButton, "saved_wifi_edit_btn")
		self.saved_wifi_cancel_btn = self.wifiWidget.findChild(QPushButton, "saved_wifi_cancel_btn")
		self.saved_wifi_del_btn = self.wifiWidget.findChild(QPushButton, "saved_wifi_del_btn")
		self.saved_wifi_save_btn = self.wifiWidget.findChild(QPushButton, "saved_wifi_save_btn")
		self.saved_wifi_status_label = self.wifiWidget.findChild(QLabel, "saved_wifi_status_label")
		self.saved_wifi_reset_btn = self.wifiWidget.findChild(QPushButton, "saved_wifi_reset_btn")
		self.saved_wifi_show_password_checkbox = self.wifiWidget.findChild(QCheckBox, "saved_wifi_show_password_checkbox")

		self.new_wifi_ssid_textedit = self.wifiWidget.findChild(QLineEdit, "new_wifi_ssid_textedit")
		self.new_wifi_psk_textedit = self.wifiWidget.findChild(QLineEdit, "new_wifi_psk_textedit")
		self.new_wifi_disable_checkbox = self.wifiWidget.findChild(QCheckBox, "new_wifi_disable_checkbox")
		self.new_wifi_calcel_btn = self.wifiWidget.findChild(QPushButton, "new_wifi_calcel_btn")
		self.new_wifi_save_btn = self.wifiWidget.findChild(QPushButton, "new_wifi_save_btn")
		self.new_wifi_status_label = self.wifiWidget.findChild(QLabel, "new_wifi_status_label")
		self.new_wifi_show_password_checkbox = self.wifiWidget.findChild(QCheckBox, "new_wifi_show_password_checkbox")

		self.ip_founder_copy_btn = self.wifiWidget.findChild(QPushButton, "ip_founder_copy_btn")
		self.ip_founder_copy_status_label = self.wifiWidget.findChild(QLabel, "ip_founder_copy_status_label")

		self.wifi_path = ""

		self.initialization()


	def initialization(self):
		self.combobox.addItem("Select the Device")
		self.combobox.addItems(drive_found.get_devices())
		self.update_device_select_label()
		self.combobox.currentIndexChanged.connect(self.update_device_select_label)
		self.refreshBtn.clicked.connect(self.refresh_device)
		self.verifyBtn.clicked.connect(lambda: self.verify_device(self.combobox.currentText()))
		self.deviceModifyBtn.clicked.connect(self.wifi_credential_UI_show)
		self.verifyStatus.setText("")
		self.verifyBtn.setEnabled(False)
		self.deviceModifyBtn.setEnabled(False)

		self.tabWidget.currentChanged.connect(self.tab_change_callback)

		self.saved_wifi_combo_box.addItem("Select WiFi")
		self.saved_wifi_combo_box.currentIndexChanged.connect(self.wifi_select_change)
		self.saved_wifi_edit_btn.clicked.connect(self.wifi_edit_btn_callback)
		self.saved_wifi_show_password_checkbox.toggled.connect(self.saved_wifi_show_password_checkbox_toggled)
		self.saved_wifi_cancel_btn.clicked.connect(self.wifi_edit_cancel_btn_callback)
		self.saved_wifi_reset_btn.clicked.connect(self.wifi_edit_reset_btn_callback)
		self.saved_wifi_save_btn.clicked.connect(self.wifi_edit_save_btn_callback)
		self.saved_wifi_del_btn.clicked.connect(self.wifi_del_btn_callback)
		self.saved_wifi_ssid_textedit.hide()
		self.saved_wifi_psk_textedit.hide()
		self.saved_wifi_edit_btn.hide()
		self.saved_wifi_cancel_btn.hide()
		self.saved_wifi_del_btn.hide()
		self.saved_wifi_save_btn.hide()
		self.saved_wifi_show_password_checkbox.hide()
		self.saved_wifi_reset_btn.hide()
		self.saved_wifi_status_label.setText("")

		self.new_wifi_save_btn.clicked.connect(self.new_wifi_save_btn_callback)
		self.new_wifi_show_password_checkbox.toggled.connect(self.new_wifi_show_password_checkbox_toggled)
		self.new_wifi_status_label.setText("")

		self.ip_founder_copy_btn.clicked.connect(self.ip_founder_copy_btn_callback)
		self.ip_founder_copy_status_label.setText("")


	def verify_device(self, directory):
		if os.path.isdir(directory + "/home/pi/"):
			self.verifyStatus.setText("<html><head/><body><p><span style='color:#177B0A;'>Device is "
									  "Okay</span></p></body></html>")
			self.deviceModifyBtn.setEnabled(True)
		else:
			self.verifyStatus.setText("<html><head/><body><p><span style='color:#ff0000;'>Device Verification Failed, "
									  "Select the correct device</span></p></body></html>")


	def refresh_device(self):
		self.combobox.clear()
		self.combobox.addItem("Select the Device")
		self.combobox.addItems(drive_found.get_devices())
		self.update_device_select_label()
		self.combobox.currentIndexChanged.connect(self.update_device_select_label)
		self.verifyStatus.setText("")
		self.verifyBtn.setEnabled(False)
		self.deviceModifyBtn.setEnabled(False)


	def update_device_select_label(self):
		if self.combobox.currentIndex() == 0:
			self.deviceSelectLabel.setText("")
			self.verifyBtn.setEnabled(False)
		else:
			self.deviceSelectLabel.setText(self.combobox.currentText())
			self.verifyBtn.setEnabled(True)

		self.verifyStatus.setText("")


	def tab_change_callback(self):
		if self.tabWidget.currentIndex() == 2:
			dest_folder_path = os.path.join(self.combobox.currentText(), "wifi_manager")
			dest_file_path = os.path.join(dest_folder_path, "ipfounder.py")
			if  not os.path.exists(dest_folder_path):
				self.ip_founder_copy_status_label.setText("<html><head/><body><p><span style='color:#ff0000;'><b>wifi_manager"
											"</b> folder is not available</span></p></body></html>")
			if os.path.exists(dest_folder_path) and not os.path.exists(dest_file_path):
				self.ip_founder_copy_status_label.setText("<html><head/><body><p><span style='color:#ff0000;'><b>ipfounder.py"
											"</b> is not available</span></p></body></html>")
			if os.path.exists(dest_folder_path) and os.path.exists(dest_file_path):
				self.ip_founder_copy_status_label.setText("<html><head/><body><p><span style='color:#177B0A;'><b>ipfounder.py"
											"</b> is already available</span></p></body></html>")


	def wifi_credential_UI_show(self):
		self.wifiWidget.move(self.mainWidget.geometry().x(),self.mainWidget.geometry().y())
		self.mainWidget.hide()
		self.wifiWidget.show()
		self.tab_change_callback()
		wifi_list = []
		self.wifi_path = self.combobox.currentText() + "/etc/wpa_supplicant/wpa_supplicant.conf"

		if os.path.isfile(self.wifi_path):
			f = open(self.wifi_path, "r")
			data = [line.strip() for line in f.read().split("\n") if line.split()]
			f.close()

			for line in range(len(data)):
				if re.findall("^network", data[line]) and re.findall("^ssid", data[line+1]):
					wifi_list.append(data[line+1][6:-1])
			self.saved_wifi_combo_box.clear()
			self.saved_wifi_combo_box.addItem("Select WiFi")
			self.saved_wifi_combo_box.addItems(wifi_list)
		else:
			self.final_status_label.setText("<html><head/><body><p><span style='color:#ff0000;'>Wifi credential "
											"file not found...</span></p></body></html>")


	def saved_wifi_show_password_checkbox_toggled(self):
		if self.saved_wifi_show_password_checkbox.isChecked():
			self.saved_wifi_psk_textedit.setEchoMode(QLineEdit.Normal)
		else:
			self.saved_wifi_psk_textedit.setEchoMode(QLineEdit.Password)


	def wifi_select_change(self):
		if self.saved_wifi_combo_box.currentIndex() != 0:
			self.saved_wifi_edit_btn.show()
			self.saved_wifi_del_btn.show()
			self.saved_wifi_ssid_textedit.hide()
			self.saved_wifi_psk_textedit.hide()
			self.saved_wifi_cancel_btn.hide()
			self.saved_wifi_save_btn.hide()
			self.saved_wifi_show_password_checkbox.hide()
			self.saved_wifi_reset_btn.hide()
			self.saved_wifi_status_label.setText("")
		else:
			self.saved_wifi_ssid_textedit.hide()
			self.saved_wifi_psk_textedit.hide()
			self.saved_wifi_edit_btn.hide()
			self.saved_wifi_cancel_btn.hide()
			self.saved_wifi_del_btn.hide()
			self.saved_wifi_save_btn.hide()
			self.saved_wifi_show_password_checkbox.hide()
			self.saved_wifi_reset_btn.hide()
			self.saved_wifi_status_label.setText("")


	def wifi_edit_btn_callback(self):
		self.saved_wifi_del_btn.hide()
		self.saved_wifi_edit_btn.hide()
		self.saved_wifi_ssid_textedit.show()
		self.saved_wifi_psk_textedit.show()
		self.saved_wifi_cancel_btn.show()
		self.saved_wifi_save_btn.show()
		self.saved_wifi_show_password_checkbox.show()
		self.saved_wifi_reset_btn.show()
		self.saved_wifi_ssid_textedit.setText(self.saved_wifi_combo_box.currentText())
		self.saved_wifi_psk_textedit.setText("")
		self.saved_wifi_status_label.setText("")


	def wifi_edit_cancel_btn_callback(self):
		self.saved_wifi_del_btn.show()
		self.saved_wifi_edit_btn.show()
		self.saved_wifi_ssid_textedit.hide()
		self.saved_wifi_psk_textedit.hide()
		self.saved_wifi_cancel_btn.hide()
		self.saved_wifi_save_btn.hide()
		self.saved_wifi_show_password_checkbox.hide()
		self.saved_wifi_reset_btn.hide()
		self.saved_wifi_ssid_textedit.setText("")
		self.saved_wifi_psk_textedit.setText("")
		self.saved_wifi_status_label.setText("")


	def wifi_edit_reset_btn_callback(self):
		self.saved_wifi_ssid_textedit.setText(self.saved_wifi_combo_box.currentText())
		self.saved_wifi_psk_textedit.setText("")


	def wifi_edit_save_btn_callback(self):
		if os.path.isfile(self.wifi_path):
			f = open(self.wifi_path, "r")
			data = [line for line in f.read().split("\n") if line.split()]
			f.close()

			for line in range(len(data)):
				if re.findall('ssid="' + self.saved_wifi_ssid_textedit.text() + '"', data[line]):
					point = re.search('psk="',data[line+1]).span()[-1]
					data[line+1] = data[line+1][:point] + str(self.saved_wifi_psk_textedit.text()) + '"'

			temp = ""
			for line in data:
				temp += str(line) + "\n"
			f = open(self.wifi_path, "w")
			f.write(temp)
			f.close()

			self.saved_wifi_del_btn.show()
			self.saved_wifi_edit_btn.show()
			self.saved_wifi_ssid_textedit.hide()
			self.saved_wifi_psk_textedit.hide()
			self.saved_wifi_cancel_btn.hide()
			self.saved_wifi_save_btn.hide()
			self.saved_wifi_show_password_checkbox.hide()
			self.saved_wifi_reset_btn.hide()
			self.saved_wifi_ssid_textedit.setText("")
			self.saved_wifi_psk_textedit.setText("")
			self.wifi_credential_UI_show()
			self.saved_wifi_status_label.setText("<html><head/><body><p><span style='color:#177B0A;'>Updated "
											"Successfully</span></p></body></html>")
		else:
			self.saved_wifi_status_label.setText("<html><head/><body><p><span style='color:#ff0000;'>Wifi credential file "
											"not found...</span></p></body></html>")


	def wifi_del_btn_callback(self):
		if os.path.isfile(self.wifi_path):
			f = open(self.wifi_path, "r")
			data = [line for line in f.read().split("\n") if line.split()]
			f.close()

			start = 0
			end = 0

			wifi_found = False
			for line in range(len(data)):
				if re.findall("^network={",data[line]):
					start = line
				if re.findall("^}",data[line]):
					end = line
					if wifi_found:
						break
				if re.findall('ssid="' + self.saved_wifi_combo_box.currentText() + '"', data[line]):
					wifi_found = True

			del data[start:end+1]

			f= open(self.wifi_path, "w")
			for i in data:
				f.write(str(i)+"\n")
			f.close()

			self.wifi_credential_UI_show()
			self.saved_wifi_status_label.setText("<html><head/><body><p><span style='color:#177B0A;'>Wifi details deleted."
											"</span></p></body></html>")
			return True
		else:
			self.saved_wifi_status_label.setText("<html><head/><body><p><span style='color:#ff0000;'>Wifi credential file "
											"not found...</span></p></body></html>")
			return False


	def new_wifi_show_password_checkbox_toggled(self):
		if self.new_wifi_show_password_checkbox.isChecked():
			self.new_wifi_psk_textedit.setEchoMode(QLineEdit.Normal)
		else:
			self.new_wifi_psk_textedit.setEchoMode(QLineEdit.Password)


	def new_wifi_save_btn_callback(self):
		if len(self.new_wifi_ssid_textedit.text()):
			data = 'network={\n\tssid="'
			data = data + self.new_wifi_ssid_textedit.text() + '"\n\tpsk="'
			data = data + self.new_wifi_psk_textedit.text() + '"\n\t'
			data = data + "key_mgmt=WPA-PSK\n}\n"

			if os.path.isfile(self.wifi_path):
				f = open(self.wifi_path, "r")
				file_data = f.read()
				f.close()

				f= open(self.wifi_path, "w")
				f.write(file_data + "\n\n" + data)
				f.close()

			self.new_wifi_ssid_textedit.setText("")
			self.new_wifi_psk_textedit.setText("")
			self.wifi_credential_UI_show()

			self.new_wifi_status_label.setText("<html><head/><body><p><span style='color:#177B0A;'>New WiFi details "
											"saved successfully</span></p></body></html>")
		else:
			self.new_wifi_status_label.setText("<html><head/><body><p><span style='color:#ff0000;'>SSID can't be blank"
											"</span></p></body></html>")
			self.new_wifi_ssid_textedit.setFocus()


	def ip_founder_copy_btn_callback(self):
		dest_folder_path = os.path.join(self.combobox.currentText(), "wifi_manager")
		src_file_path = os.path.join(self.src_path, "ipfounder.py")
		if  not os.path.exists(dest_folder_path):
			os.mkdir(dest_folder_path)
		os.popen("cp " + src_file_path + " " + dest_folder_path)
		time.sleep(1)
		self.ip_founder_copy_status_label.setText("<html><head/><body><p><span style='color:#177B0A;'><b>ipfounder.py"
											"</b> is copied to the location</span></p></body></html>")


if __name__ == '__main__':
	if os.getuid() != 0:
		print("Permission Denied\nRun as Super User")
		sys.exit()
	else:
		app = QApplication(sys.argv)
		window = Ui()
		sys.exit(app.exec_())
