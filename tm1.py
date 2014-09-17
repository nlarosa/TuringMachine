#!/usr/bin/python

# Nicholas LaRosa
# Eric Krakowiak
# CSE 30151
# Project 3

import sys
import re
import os
import math
from TM import TM

if len(sys.argv) != 2:
	raise Exception('Usage: tm.py <tm_description>\n')

location = sys.argv[1]

ourTM = TM( )

if ourTM.processFile( location ):

	#print( 'File processed.' )
	#ourTM.printDescription()
	ourTM.getInput()

