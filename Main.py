import RPi.GPIO as GPIO
import time
import os
import Adafruit_MCP3008

# Check for secure mode or unsecure mode
# secure mode: button pressed
# unsecure mode: button + knob 
Sbtn = False
Ubtn = False
def ServicePress(channel):

	print("Secure mode!")
	global Sbtn, code, Time 
	Sbtn = True
	Ubtn = False
	code = []
	Time = []

def unsecure(channel):
	print("Unsecure mode!")
	global Ubtn, code, Time 
	Ubtn = True
	Sbtn = False
	code = []
	Time = []


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


def Buzz(answer):
	if (answer):
		os.system("omxplayer correctAns.mp3")
	else:
		os.system("omxplayer wrongAns.mp3")
	#os.system("q")



################################  Main  ######################################

# main function to check buttons
# Assume lock is locked by default
# keep log of durations in ms
def main():

	counter = 0

	while (1):
    	
		global ch0, Sbtn, code, inputCode, interval, Ubtn, Time, ans, unlockPin, lockPin
		ch0.insert(16, mcp.read_adc(0))
		ch0.pop(0)

		#if button pressed then measure turn
		
		fin = [0] * 16
		check = -1
		lastValue = -2


		# If btn pressed check for turns
		if ((Sbtn == True) or (Ubtn == True)):

			print("Start!")
			init = mcp.read_adc(0)
			ch0.insert(16, init)
			ch0.pop(0)
			 #make sure not off (0V) initially for now

			time.sleep(0.5)
			interval = 0
			while (1):
				
				time.sleep(0.5)
				fin = mcp.read_adc(0)
				
				ch0.insert(16, fin)
				ch0.pop(0)


				os.system("clear")
				lastValue = check

				check = checkTurn(init, fin)
				counter += 0.5
				interval += 0.5
				# Compare last turn to current turn
				if ((lastValue != check) and (lastValue != 2)):
					counter = 0
					Time.append(interval - 0.5)
					interval = 0

				if ((lastValue != check) and (lastValue == 2)):
					interval = 0
					counter = 0


				init = fin
				if (check != 2):
					code.append(check)  #0 = left, 1 = right, 2 = no turn
				
				if ((lastValue == check) and (lastValue != 2)):
					code.pop()

				inputCode = True
				print("Check " + str(check))
				print("Time passed: " + str(counter) + "s")

				if (check == 2) and (interval > 4.5):
					break
				

			#compare code
			if (inputCode == True):
				
				del(Time[0])

				#Sort the input
				if (Ubtn):
					Time.sort()
					lockTime.sort()

				if ((code == lock) and (lockTime == Time) and Sbtn):
					GPIO.output(lockPin, GPIO.LOW)
					print("Code and Timing correct!")
					ans = True
					inputCode = False

					# Unlock line high for 2s
					GPIO.output(unlockPin, GPIO.HIGH)
					time.sleep(2)
					GPIO.output(unlockPin, GPIO.LOW)


				elif ((lockTime == Time) and Ubtn):
					GPIO.output(lockPin, GPIO.LOW)
					print("Timing correct!")
					ans = True
					inputCode = False

					GPIO.output(unlockPin, GPIO.HIGH)
					time.sleep(2)
					GPIO.output(unlockPin, GPIO.LOW)

				else:
					ans = False
					print("Wrong code!")
					

					GPIO.output(lockPin, GPIO.HIGH)
					time.sleep(2)
					GPIO.output(lockPin, GPIO.LOW)

				# Play a sound
				Buzz(ans)
				ans = False



			Sbtn = False
			Ubtn = False
			print("Done comparing!")
			print("Code entered: ")
			print(code)
			print("interval: ")
			print(Time)
			time.sleep(1.5)


########################### Initial Setup #################################

#Globals
#GPIO.cleanup()
Time = []

ch0 = [0]*16 # Channel for the knob
lock = [0,1,0,1]
lockTime = [2,2,2,2]
ans = False
code = []  # Code input by user
GPIO.setmode(GPIO.BCM)
interval = 0 # Time passed
# Buttons definition
service = 2 # Can change later on
GPIO.setup(service, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(service, GPIO.FALLING, callback = ServicePress, bouncetime = 500)

Upin = 26
GPIO.setup(Upin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(Upin, GPIO.FALLING, callback = unsecure, bouncetime = 500)


   #Lock and unlock ports to be done (Lock on by default)
lockPin = 3
inputCode  =  False

unlockPin = 19


GPIO.setup(unlockPin, GPIO.OUT)
GPIO.output(unlockPin, GPIO.LOW)


GPIO.setup(lockPin, GPIO.OUT)
GPIO.output(lockPin, GPIO.LOW)
print("LOCKED!")


GPIO.output(lockPin, GPIO.HIGH)
time.sleep(2)
GPIO.output(lockPin, GPIO.LOW)
    # Software SPI configuration (in BCM mode):
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

########################### Execution ####################################

if __name__ == "__main__":
	main()