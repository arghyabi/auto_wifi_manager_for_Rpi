import psutil
import re


def get_devices():
	device_num = 0
	devices = []
	for i in psutil.disk_partitions():
		if re.findall("/media/", i[1]):
			devices.append(i[1])
			device_num += 1

	if device_num == 0:
		print("NO DEVICE FOUND!")

	return devices
