import RPi.GPIO as GPIO
import time
import os
import Adafruit_MCP3008


def secureMode(channel):
	global Sbtn, code, Time, interval, counter, Ubtn
	Sbtn = True
	Ubtn = False
	code = []
	Time = []
	interval = 0
	counter = 0

def unsecureMode(channel):
	global Ubtn, code, Time, interval, counter, Sbtn
	Ubtn = True
	Sbtn = False
	code = []
	Time = []
	interval = 0
	counter = 0


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
	#os.system("q")                                                                                         #Delete This
		
def ModeDisplay():
        if (Sbtn == True):
                f = open('SBtn.txt','r')
                DisplayMode = f.read()
                print(DisplayMode)
                f.close()
        elif (Ubtn == True):
                f = open('UBtn.txt','r')
                DisplayMode = f.read()
                print(DisplayMode)
                f.close()                

################################  Main  ######################################

# main function to check buttons
# Assume lock is locked by default
# keep log of durations in ms
def main():
        #Wait for mode button press
        #Loops until keyboard interrupt
	while (1):
                global Sbtn, code, inputCode, interval, Ubtn, Time, ans, unlockPin, lockPin, interval, counter
		#global ch0, Sbtn, code, inputCode, interval, Ubtn, Time, ans, unlockPin, lockPin, interval, counter, mode

		#Indicate that the device is locked
		#print("LOCKED!")
		#os.system('clear')
		
		#Create a queue of 16 elements (first in - first out)                                           #Delete this
		#ch0.insert(16, mcp.read_adc(0))
		#ch0.pop(0)

		#if button pressed then measure turn
		#fin = [0] * 16

		#Determine which direction the Dial has moved, -1 indicates error
		check = -1
		#The previous turn direction of Dial (0,1,2)
		lastValue = -2


		#If Secure/Unsecure button pressed check for turns
		if ((Sbtn == True) or (Ubtn == True)):
			print("Start!")
			init = mcp.read_adc(0)
			
			#ch0.insert(16, init)                                                                   #Delete this
			#ch0.pop(0)
			#make sure not off (0V) initially for now

			#loops until there is no turn of dial for 5[s] (500[ms] discrete time iteration)
			while (1):
				
				time.sleep(0.5)
				fin = mcp.read_adc(0)
				
				#ch0.insert(16, fin)                                                             #Delete this
				#ch0.pop(0)


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
				#Display Metadata during mode operation
				print("Check " + str(check))
				print("Time passed: " + str(counter) + "s")
				ModeDisplay()
				
				if (check == 2) and (interval > 4.5):
					break
				

			#compare code
			if (inputCode == True):
				if ((len(Time)>0) and (Time[0] < 0.5)):                                                                       
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
					print("Wrong Combination!")
					

					GPIO.output(lockPin, GPIO.HIGH)
					time.sleep(2)
					GPIO.output(lockPin, GPIO.LOW)

				#Play a sound
				Buzz(ans)
				#Reset ans
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

#Global init

#Dynamic Arrays of the combination inserted by the user
Time = []
code = []

#Hard Coded Combination
lock = []
lockTime = []

#Secure button
Sbtn = False
#Unsecure button
Ubtn = False

#Elapsed time
counter = 0
interval = 0

#mode = "Select Mode"                                                                                                   #Delete This
ans = False
inputCode  =  False
#Redundant array                                                                                                        #Delete this
#ch0 = [0]*16 # Channel for the knob

#Raspberry setup
GPIO.setmode(GPIO.BCM)

# Buttons definition
securePin = 2
GPIO.setup(securePin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(securePin, GPIO.FALLING, callback = secureMode, bouncetime = 500)

unsecurePin = 26
GPIO.setup(unsecurePin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(unsecurePin, GPIO.FALLING, callback = unsecureMode, bouncetime = 500)


#Lock and unlock ports to be done (Lock on by default)
#Red LED
lockPin = 3
GPIO.setup(lockPin, GPIO.OUT)
GPIO.output(lockPin, GPIO.LOW)
#Blue Led
unlockPin = 19
GPIO.setup(unlockPin, GPIO.OUT)
GPIO.output(unlockPin, GPIO.LOW)


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
