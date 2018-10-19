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
	print("Initial: " + str(initial) + "        Final: " + str(final))
	# Allowed tolerance for small negligable changes
	tolerance = 10
	if (initial - final > tolerance):
		print("Left turn")
		return 0 # Left turn
	elif (final - initial > tolerance):
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
    	
		global ch0, Sbtn, code, ans, interval
		ch0.insert(16, mcp.read_adc(0))
		ch0.pop(0)

		#if button pressed then measure turn
		
		fin = [0] * 16
		check = -1
		lastValue = -1


		# If btn pressed check for turns
		if (Sbtn == True):

			print("Start!")
			init = mcp.read_adc(0)
			ch0.insert(16, init)
			ch0.pop(0)
			 #make sure not off (0V) initially for now

			time.sleep(1)
			interval = 0
			while (1):
				

				time.sleep(1)
				fin = mcp.read_adc(0)
				ch0.insert(16, fin)
				ch0.pop(0)


				os.system("clear")
				lastValue = check

				check = checkTurn(init, fin)

				interval += 1
				# Compare last turn to current turn
				if (lastValue != check):
					Time.append(interval)
					interval = 0

				init = fin
				if (check != 2):
					code.append(check)  #0 = left, 1 = right, 2 = no turn
				
				ans = True
				print("Check " + str(check))

				if (check == 2) and (interval > 5):
					break
				

			#compare code
			if (ans == True):
				
				del(code[0])

				if (code == lock):
					GPIO.output(lockPin, GPIO.LOW)
					print("Code correct!")
					ans = False
				else:
					print("Wrong code!")


			Sbtn = False
			print("Done comparing!")
			print("Code entered: ")
			print(code)
			print("interval: ")
			print(Time)



########################### Initial Setup #################################

#Globals
Time = [2]
Timer = [0]*16
ch0 = [0]*16 # Channel for the knob
lock = [0,1,0,1]
code = [2]  # Code input by user (2 = start or stop)
GPIO.setmode(GPIO.BCM)
interval = 0 # Time passed
# Buttons definition
service = 2 # Can change later on
GPIO.setup(service, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(service, GPIO.FALLING, callback = ServicePress, bouncetime = 500)
    

   #Lock and unlock ports to be done (Lock on by default)
lockPin = 3
ans  =  False
GPIO.setup(lockPin, GPIO.OUT)
GPIO.output(lockPin, GPIO.HIGH)
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