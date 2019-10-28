import RPi.GPIO as GPIO
import time
import os

from subprocess import check_output

# Define GPIO to LCD mapping
LCD_RS = 12
LCD_E  = 16
LCD_D4 = 18 
LCD_D5 = 22
LCD_D6 = 11
LCD_D7 = 13
LED_ON = 40

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def execute(cmd):
	res = os.popen(cmd).read().strip()
	return res

def main():
	# Main program block

	# Initialise display
  	lcd_init()
	while True:
		try:
			ssid = execute("iwconfig wlan0").split("\n")[0].split('"')[-2]
			#print(ssid)
			whoami = execute("whoami")
			line_1_data = whoami + ' "' + ssid + '"'
			ip = execute("ifconfig wlan0").split("\n")[1].split()[1][5:]
			if len(ip) < 7:
				ip = "No IP Found"
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(line_1_data, 2)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string(ip, 2)
			# time.sleep(2)		
  			# Toggle backlight on-off-on
			GPIO.output(LED_ON, True)
  			time.sleep(1)
			GPIO.output(LED_ON, False)
			time.sleep(1)
		except:
			pass

def lcd_init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)       # Use BCM GPIO numbers
	GPIO.setup(LCD_E, GPIO.OUT)  # E
	GPIO.setup(LCD_RS, GPIO.OUT) # RS
	GPIO.setup(LCD_D4, GPIO.OUT) # DB4
	GPIO.setup(LCD_D5, GPIO.OUT) # DB5
	GPIO.setup(LCD_D6, GPIO.OUT) # DB6
	GPIO.setup(LCD_D7, GPIO.OUT) # DB7
	GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable  
	# Initialise display
	lcd_byte(0x33,LCD_CMD)
	lcd_byte(0x32,LCD_CMD)
	lcd_byte(0x28,LCD_CMD)
	lcd_byte(0x0C,LCD_CMD)  
	lcd_byte(0x06,LCD_CMD)
	lcd_byte(0x01,LCD_CMD)  

def lcd_string(message,style):
	# Send string to display
	# style=1 Left justified
	# style=2 Centred
	# style=3 Right justified

	if style==1:
		message = message.ljust(LCD_WIDTH," ")  
	elif style==2:
		message = message.center(LCD_WIDTH," ")
	elif style==3:
		message = message.rjust(LCD_WIDTH," ")

	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
	# Send byte to data pins
	# bits = data
	# mode = True  for character
	#        False for command

	GPIO.output(LCD_RS, mode) # RS

	# High bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x10==0x10:
		GPIO.output(LCD_D4, True)
	if bits&0x20==0x20:
		GPIO.output(LCD_D5, True)
	if bits&0x40==0x40:
		GPIO.output(LCD_D6, True)
	if bits&0x80==0x80:
		GPIO.output(LCD_D7, True)

	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)  
	time.sleep(E_DELAY)      

	# Low bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x01==0x01:
		GPIO.output(LCD_D4, True)
	if bits&0x02==0x02:
		GPIO.output(LCD_D5, True)
	if bits&0x04==0x04:
		GPIO.output(LCD_D6, True)
	if bits&0x08==0x08:
		GPIO.output(LCD_D7, True)

	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)  
	time.sleep(E_DELAY)   

if __name__ == '__main__':
	main()
