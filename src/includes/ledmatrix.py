#
# ledmatrix.py - Custom LED Matrix Controller 
#
# Author: Jaakko Hartikainen (jaakko.hartikainen@gmail.com)
#
# Based on Pete Goss's original code (see http://www.embeddedadventures.com/Tutorials/tutorials_detail/184 )  

import sys
import time

# Modify this import row to change font!
import fontv as fontv

import RPi.GPIO as gpio
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

###################################################
# Give the GPIO pins labels that match the LDP-8008
###################################################
R1=11   
G1=12   
EN=8  
A=3  
B=5  
C=7  
D=10  
L=13  
S=15  

####################################
# init function
# usage: init_gpio()
# initialises the LDP-8008 <---> RPio library mapping
####################################

def init_gpio():
	# set GPIO pins as outputs
	gpio.setup(R1,gpio.OUT)
	gpio.setup(G1,gpio.OUT)
	gpio.setup(EN,gpio.OUT)
	gpio.setup(A,gpio.OUT)
	gpio.setup(B,gpio.OUT)
	gpio.setup(C,gpio.OUT)
	gpio.setup(D,gpio.OUT)
	gpio.setup(L,gpio.OUT)
	gpio.setup(S,gpio.OUT)

	#initialise the output pins
	gpio.output(R1,1)
	gpio.output(G1,1)
	gpio.output(S,1)
	gpio.output(L,0)
	gpio.output(EN,0)
	clear()
####################################
# end init function
####################################


####################################
# clear function
# usage: clear()
# function sets the shift register 
# bits to blank and turns off display
####################################
def clear():
		gpio.output(R1,1)
		gpio.output(G1,1)
		for i in range(80):
			gpio.output(S,1)
			gpio.output(S,0)
			gpio.output(S,1)
		displayoff()
####################################
# end init function
####################################


####################################
# shift function
# usage: shift()
# function shifts the current led colour 
# into the first column of the register
####################################
def shift():
		gpio.output(S,1)
		gpio.output(S,0)
		gpio.output(S,1)
####################################
# end shift function
####################################

####################################
# colour function
# usage: colour(colour_value)
# sets the current led colour 
# 0=blank 1=red 2=green 3=orange
####################################
def colour(n):
	if n == 3: #orange	
		gpio.output(R1,0)
		gpio.output(G1,0)
	elif n == 2: #green
		gpio.output(R1,1)
		gpio.output(G1,0)
	elif n == 1: #red
		gpio.output(R1,0)
		gpio.output(G1,1)
	else: # off
		gpio.output(R1,1)
		gpio.output(G1,1)
####################################
# end colour function
####################################

####################################
# colourshift function
# usage: colourshift(colour_value)
# sets the current led colour 
# and also shifts it into the register
# 0=blank 1=red 2=green 3=orange
####################################
def colourshift(n):
	if n == 3: #orange	
		gpio.output(R1,0)
		gpio.output(G1,0)
	elif n == 2: #green
		gpio.output(R1,1)
		gpio.output(G1,0)
	elif n == 1: #red
		gpio.output(R1,0)
		gpio.output(G1,1)
	else: # off
		gpio.output(R1,1)
		gpio.output(G1,1)
	gpio.output(S,1)
	gpio.output(S,0)
	gpio.output(S,1)
####################################
# end colour function
####################################

####################################
# showrow function
# usage: showrow(row_value)
# displays the register on a row 
# row_value = 0-7
####################################
def showrow(n):
	if n == 7:
		gpio.output(A,1)
		gpio.output(B,1)
		gpio.output(C,1)
		gpio.output(D,0)
	elif n == 6:
		gpio.output(A,0)
		gpio.output(B,1)
		gpio.output(C,1)
		gpio.output(D,0)
	elif n == 5:
		gpio.output(A,1)
		gpio.output(B,0)
		gpio.output(C,1)
		gpio.output(D,0)
	elif n == 4:
		gpio.output(A,0)
		gpio.output(B,0)
		gpio.output(C,1)
		gpio.output(D,0)
	elif n == 3:
		gpio.output(A,1)
		gpio.output(B,1)
		gpio.output(C,0)
		gpio.output(D,0)
	elif n == 2:
		gpio.output(A,0)
		gpio.output(B,2)
		gpio.output(C,0)
		gpio.output(D,0)
	elif n == 1:
		gpio.output(A,1)
		gpio.output(B,0)
		gpio.output(C,0)
		gpio.output(D,0)
	else:
		gpio.output(A,0)
		gpio.output(B,0)
		gpio.output(C,0)
		gpio.output(D,0)
	# latch the data
	gpio.output(L,1)
	gpio.output(L,0)
	# display the row
	gpio.output(EN,1)
####################################
# end showrow function
####################################

####################################
# displayoff function
# usage: displayoff()
# turns off the display 
####################################
def displayoff():
	gpio.output(EN,0)
####################################
# end displayoff function
####################################

####################################
# displayon function
# usage: displayon()
# turns on the display 
####################################
def displayon():
	gpio.output(EN,1)
####################################
# end displayon function
####################################

# This matrix is a representation of the led's that are lit on the 80x8 display
#
matrix=[[0 for i in range(80)] for i in range(8)]
#
# Function to shift left all the values of the matrix array
# this allows us to put new data in the first column
#
def shiftmatrix():
	for row in range(8):
		for col in range(79,0,-1):
			matrix[row][col]=matrix[row][col-1]
# end def

# Function to read the matrix array and output the values to the display device
#
def showmatrix():
	displayoff()
	for row in reversed(range(8)):
		for col in reversed(range(80)):
			colourshift(matrix[row][col])
		showrow(row)
# end def

# Methods for actually operating the screen start here 

def initledmatrix():
	init_gpio()
# end def

def scroll(message, colour, repeats):
	
	# textinput=str("Placeholder for testing Python code 1234567890")
	textinput=message
	colour=int(colour)
	
	# Append extra characters to text input to allow for wrap-around
	textinput+='  ::  '

	# save the ascii values of the input characters into the inputarray 
	# the font module uses the ascii value to index the font array
	inputarray=[]
	for char in textinput:
		inputarray.append(ord(char))

	# dotarray is  8 X n
	# n is determined by the number of characters multiplyed by 8 
	# n will be len(dotarray[0]) after filling dotarray from characters
	# in the inputarray
	#
	dotarray=[[] for i in range(8)]
	#
	# fill the dot array with the colour digits
	# this is the dot pattern that we want to show
	#
	for row in range(8):
		for ascii in inputarray:
			# get the width of the character from the first element of the font variable
			width=fontv.array[ascii][0]
			binary='{0:{fill}{align}{width}{base}}'.format(fontv.array[ascii][row+1],base='b',fill='0',align='>',width=width)
			for digit in range(width):
				if binary[digit] == '0':
					dotarray[row].append(0)
				else:
					dotarray[row].append(colour)
	#
	# Continually output to the display until Ctrl-C
	#

	loop=0;

	while (loop < repeats):
		try:
			# loop around each column in the dotarray
			for col in range(len(dotarray[0])):
				for row in range(8):
					# copy the current dotarray column values to the first column in the matrix
					matrix[row][0]=(dotarray[row][col])
				# now that we have updated the matrix lets show it
				showmatrix()
				# shift the matrix left ready for the next column
				shiftmatrix()
			loop += 1	
		except KeyboardInterrupt:
			clear()
			print
			print("Finished")
	clear()
#end def