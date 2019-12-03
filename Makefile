all:
	pyinstaller -F --distpath . auto_wifi_manager.py
	sudo rm -r build/ __pycache__/
	sudo rm auto_wifi_manager.spec

install:
	sudo mkdir -p /usr/share/auto_wifi_manager
	sudo cp *.ui /usr/share/auto_wifi_manager/
	sudo cp Wifi-Logo.png /usr/share/auto_wifi_manager/

clean:
	rm auto_wifi_manager

uninstall:
	sudo rm -r /usr/share/auto_wifi_manager
