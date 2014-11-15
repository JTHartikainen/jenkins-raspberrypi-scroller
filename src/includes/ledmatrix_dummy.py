#
# ledmatrix_dummy.py - Custom LED Matrix Controller (dummy, for development)
#
# Author: Jaakko Hartikainen (jaakko dot hartikainen at gmail dot com )
#

import sys
import time
import logging

def initledmatrix():
	print("Dummy initledmatrix invoked.")

def scroll(message, colour, repeats):
	print("[LED SCROLL] message: " + message + ", colour: " + str(colour) + ", repeats: " + str(repeats))
