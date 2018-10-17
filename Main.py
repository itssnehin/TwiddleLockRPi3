import RPi.GPIO as GPIO
import time
import os
import Adafruit_MCP3008

# Check for secure mode or unsecure mode
# secure mode: button pressed
# unsecure mode: button + knob 
Sbtn = False

def ServicePress(channel):
	#print(ch0)
	global Sbtn
	Sbtn = True



# Determines if the knob is turned left(0) or right (1)
# take in two lists and compare
def checkTurn(initial, final):
	#print("Initial: " + str(initial) + "        Final: " + str(final))
	if (initial > final):
		print("Left turn")
		return 0 # Left turn
	elif (initial < final):
		print("Right turn")
		return 1 # right turn
	else:
		print("No turn")
		return 2 # no change in position


# Knob has 20 possible 'signals'
# R10 - R1 and L1 to L10s
#def CodeLine():



#def UnlockLine():



#def LockLine():



#def SecureMode():



# main function to check buttons
# Assume lock is locked by default
# keep log of durations in ms
def main():



	while (1):
    	
		global ch0, Sbtn
		ch0.insert(16, mcp.read_adc(0))
		ch0.pop(0)

		#if button pressed then measure turn
		
		fin = [0] * 16
		check = -1



		# If btn pressed check for turns
		if (Sbtn == True):

			init = mcp.read_adc(0)
			ch0.insert(16, init)
			ch0.pop(0)
			 #make sure not off (0V) initially for now

			time.sleep(1)
			
			while (1):
				
				time.sleep(2)
				fin = mcp.read_adc(0)
				ch0.insert(16, fin)
				ch0.pop(0)


				check = checkTurn(init, fin)
				init = fin
				


			Sbtn = False
			print("Done comparing!")



########################### Initial Setup #################################

#Globals
Time = [0]*16
Timer = [0]*16
ch0 = [0]*16 # Channel for the knob
GPIO.setmode(GPIO.BCM)

# Buttons definition
service = 2 # Can change later on
GPIO.setup(service, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(service, GPIO.FALLING, callback = ServicePress, bouncetime = 500)
    

   #Lock and unlock ports to be done (Lock on by default)
lock = 3
GPIO.setup(lock, GPIO.OUT)
GPIO.output(lock, GPIO.HIGH)
print("LOCKED!")

    # Software SPI configuration (in BCM mode):
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

########################### Execution ####################################

if __name__ == "__main__":
	main()