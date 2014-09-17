#!/usr/bin/env python

# Nicholas LaRosa
# Eric Krakowiak
# CSE 30151
# Project 3

import os
import sys

class TM:
	
	def __init__(self, name = 'Turing Machin'):					# represents a complete TM definition
		
		self.name = name
		self.states = list()					# Q
		self.inputAlphabet = list()				# Sigma
		self.tapeAlphabet = list()				# Gamma
		self.transitions = list()				# Transitions
		self.startState = ""					# q0
		self.acceptState = ""					# F						# one accept and one reject
		self.rejectState = ""					# F

	def getName(self):
		
		return self.name

	def processFile(self, fileName):			# file will be processed for NFA definition
		
		file = open(fileName)
		lines = file.readlines()				# lines array contains entire file

		for line in lines:
		
			if line[0] == 'A':
		
				if self.addInputAlphabet(line.rstrip()) == 0:

					return 0
		
			elif line[0] == 'Z':
			
				if self.addTapeAlphabet(line.rstrip()) == 0:

					return 0
			
			elif line[0] == 'Q':
			
				if self.addStates(line.rstrip()) == 0:

					return 0
		
			elif line[0] == 'T':
		
				if self.addTransition(line.rstrip()) == 0:

					return 0
		
			elif line[0] == 'S':
		
				if self.addStartState(line.rstrip()) == 0:

					return 0
		
			elif line[0] == 'F':
		
				if self.addAccRejState(line.rstrip()) == 0:

					return 0
		
			else:
		
				print('State syntax: "Q:" followed by comma-separated states.')
				print('Input Alphabet syntax: "A:" followed by comma-separated input symbols.')
				print('Tape Alphabet syntax: "Z:" followed by comma-separated tape symbols.')
				print('Transition syntax: "T:" followed by comma-separated start state, cur. tape symbol, result. state, symbol to be written to tape, and tape head dir.')
				print('Start state syntax: "S:" followed by a state.')
				print('Accept state syntax: "F:" followed by comma-separated accept state and reject state, in that order.')
				return 0

		if self.testTransitions() == 0:

			#print( 'Non-deterministic.' )
			return 0							# non-deterministic

		else:

			#print( 'Deterministic.' )
			return 1							# deterministic

	def getInput(self):							# process a single set of tape input
		
		if len(self.states) == 0:
		
			print('Establish state list via addStates().')
			return 0
		
		if len(self.inputAlphabet) == 0:
		
			print('Establish input alphabet via addInputAlphabet().')
			return 0
		
		if len(self.tapeAlphabet) == 0:
		
			print('Establish tape alphabet via addTapeAlphabet().')
		
		if len(self.transitions) == 0:
		
			print('Establish transition rules via addTransition().')
			return 0
		
		if len(self.startState) == 0:
		
			print('Establish start state via addStartState().')
			return 0
		
		if self.acceptState == "" or self.rejectState == "":
		
			print('Establish accept and reject states via addAccRejState().')
			return 0

		line = sys.stdin.readline()

		try:
		
			line = int(line)					# confirm first line as integer
		
		except ValueError:
		
			print('Invalid input tape declaration.')
			print('First line in an input tape is an integer representing the number of following tape lines.')
			return 0

		output = ''								# string will be built containing output

		#print( 'Number of Lines: ' + str( line ) )	
	
		for lineNum in range(line):
			
			line = sys.stdin.readline()
			newOutput = self.processInputLine(line.rstrip())
		
			if newOutput != '':
		
				output = output + newOutput
		
			else:
	
				return 0
		
			output = output + '\n'
		
		sys.stdout.write( output )
	
	def processInputLine(self, tapeString):		# each input line results in state listing
	
		currState = self.startState
		transitionTaken = self.transitions[0]	# each input will result in a transition b/c of DPDA

		#print( 'Procesing: ' + tapeString )
		tape = tapeString.split(',')
		
		for symbol in tape[:]:

			if symbol == '':

				tape.remove( symbol )

			elif symbol not in self.inputAlphabet:

				return 'Error: Input tape contains non-alphabet symbol: ' + symbol

		output = ''

		tapeHeadIndex = 0							# tape head starts at leftmost tape
		
		transitionCount = 0
		transitionCountLimit = 1000					# transition count limit

		# PRINT FIRST LINE

		output = '()' + currState + '('
		
		for symbol in tape[:-1]:

			output = output + symbol + ','

		output = output + tape[-1] + ')\n'			# print first line with head at 0

		while( currState != self.acceptState and currState != self.rejectState and transitionCount < transitionCountLimit ):	
																# no transitions from accept or reject allowed
			transitionFound = False								# if no transition found, REJECT!
			tapeHead = tape[ tapeHeadIndex ]

			for transition in self.transitions:

				if transition[ 'startState' ] == currState:		# deal with transitions only on this state

					if transition[ 'currTapeSymbol' ] == tapeHead:	# and on tape symbol
	
						transitionFound = True
						transitionCount = transitionCount + 1
						#print transitionCount

						currState = transition[ 'resultState' ]						# make transition
						tape[ tapeHeadIndex ] = transition[ 'writTapeSymbol' ]		# write new symbol
						
						if transition[ 'headDirection' ].upper() == 'L':

							if tapeHeadIndex == 0:									# left at front

								tape = [ ' ' ] + tape								# add space at 0
							
							else:

								tapeHeadIndex = tapeHeadIndex - 1

						else:

							if tapeHeadIndex == len( tape ) - 1:					# right at end

								tape.append( ' ' )									# add space at back
							
							tapeHeadIndex = tapeHeadIndex + 1

						break			
	
			if not transitionFound:						# did not find a transition on input, exit

				tapeHeadIndex = tapeHeadIndex + 1 
				currState = self.rejectState

			output = output + '('						# START PRINTING

			for i in range( len( tape[0:tapeHeadIndex] ) ):		# all characters preceding tapeHead

				if i == tapeHeadIndex - 1:

					output = output + tape[i] + ')'							# end with paren, not comma

				else:

					output = output + tape[i] + ','	

			if tapeHeadIndex == 0:

				output = output + ')'

			output = output + currState

			#print tape
			#print tapeHeadIndex

			rightSide = tape[tapeHeadIndex:]
			rightString = ')'								# we build the righthand string in reverse
			count = 0
			nonBlankFound = False

			for symbol in rightSide[::-1]:					# all characters after tapeHead

				if symbol != ' ':							# print symbol under head to rightmost non-blank

					if count == 0:

						rightString = symbol + rightString

					else:

						rightString = symbol + ',' + rightString

					count = count + 1
					nonBlankFound = True

				elif nonBlankFound:

					rightString = symbol + ',' + rightString	# we can print blank characters to the left of a non-blank character

			#if tape[-1] != ' ' and tapeHeadIndex < len( tape ):	# last symbol, if non-blank and necessary

			#	output = output + tape[-1] + ')\n'				# end with paren, not comma

			#else:

			#	output = output + ')\n'
		
			rightString = '(' + rightString

			output = output + rightString + '\n'

		if currState == self.acceptState:

			output +=  'ACCEPT\n'

		elif currState == self.rejectState:

			output += 'REJECT\n'

		else:

			output += 'DID NOT HALT\n'

		return output

	# ADD FUNCTIONS

	def addStates(self, stateString):				# format - Q;q1,q2,q3...
		
		if stateString[0] != 'Q':
		
			print('State syntax: "Q:" followed by comma-separated states.')
			return 0
		
		else:
		
			states = stateString[2:].split(',')
		
			for state in states:
		
				self.states.append(state)
		
			return 1

	def addInputAlphabet(self, alphabetString):		# format - A:0,1...
		
		if alphabetString[0] != 'A':
		
			print('Input alphabet syntax: "A:" followed by comma-separated symbols.')
			return 0
		
		else:
		
			symbols = alphabetString[2:].split(',')
		
			for symbol in symbols:

				self.inputAlphabet.append(symbol)
		
			return 1

	def addTapeAlphabet(self, alphabetString):		# format - Z:0,1...
			
		if alphabetString[0] != 'Z':
			
			print('Tape alphabet syntax: "Z:" followed by comma-separated symbols.')
			return 0
		
		else:
		
			symbols = alphabetString[2:].split(',')
		
			for symbol in symbols:
		
				self.tapeAlphabet.append(symbol)
		
			return 1

	def addTransition(self, transitionString):
		
		if transitionString[0] != 'T':
			
			print('Transition syntax: "T:" followed by comma-separated start state, cur. tape symbol, result. state, symbol to be written to tape, and tape head dir.')
			return 0
		
		elif len(self.states) == 0 or len(self.inputAlphabet) == 0 or len(self.tapeAlphabet) == 0:	# alphabet and state list must be established
		
			print('Establish input alphabet, tape alphabet and states via addInputAlphabet(), addTapeAlphabet() and addStates(), respectively.')
			return 0
		
		else:
			
			transition = transitionString[2:].split(',')								# just get the 5 states/symbols
	
			if len(transition) != 5:
				
				print('Transition syntax: "T:" followed by comma-separated start state, cur. tape symbol, result. state, symbol to be written to tape, and tape head dir.')
				return 0
			
			elif transition[0] in self.states and \
					( transition[1] in self.inputAlphabet or transition[1] in self.tapeAlphabet or transition[1] == ' ' ) and \
					transition[2] in self.states and \
					( transition[3] in self.inputAlphabet or transition[3] in self.tapeAlphabet or transition[3] == ' ' ) and \
					( transition[4].upper() == 'R' or transition[4].upper() == 'L' ):

				currTransition = {}														# each transition represented by dictionary

				try:

					currTransition[ 'startState' ] = transition[0]
					currTransition[ 'currTapeSymbol' ] = transition[1]
					currTransition[ 'resultState' ] = transition[2]
					currTransition[ 'writTapeSymbol' ] = transition[3]
					currTransition[ 'headDirection' ] = transition[4]

					for transition in self.transitions:									# prevent the entering of duplicate transition

						if currTransition != transition:

							#print( 'Current transition added.' )
							self.transitions.append( currTransition )
							break

					if len( self.transitions ) == 0:

						self.transitions.append( currTransition )

				except Exception as ex:

					print 'addTransition() error: ' + str( ex )
					return 0

			else:

				print('Length of line: ' + str( len( transition ) ) )
				print('States: ' + str( self.states ) )
				print('Input Alphabet: ' + str( self.inputAlphabet ) )
				print('Tape Alphabet: ' + str( self.tapeAlphabet ) )
				print('Failed configuration at transition: ' + str( transition ) )
				print('Establish input alphabet, tape alphabet and states via addInputAlphabet(), addTapeAlphabet() and addStates(), respectively.')
				return 0

	def addStartState(self, startString):
	
		if startString[0] != 'S':
	
			print('Start state syntax: "S:" followed by a state.')
			return 0
	
		else:
	
			start = startString[2:].split(',')
	
			if len(start) != 1:
		
				print('Only one start state allowed per TM.')
				return 0
	
			elif start[0] in self.states:
	
				self.startState = start[0]
				return 1
	
			else:
	
				print('Establish state list via addStates().')
				return 0

	def addAccRejState(self, acceptString):
		
		if acceptString[0] != 'F':
		
			print('Accept state syntax: "F:" followed by comma-separated accept state and reject state, in that order.')
			return 0
		
		else:
		
			accepts = acceptString[2:].split(',')
		
			if len(accepts) != 2:

				print('Accept state syntax: "F:" followed by comma-separated accept state and reject state, in that order.')
				return 0

			self.acceptState = accepts[0]
			self.rejectState = accepts[1]
		
			return 1

	# TRANSITION HELPERS

	def testTransitions( self ):

		for i in range( len( self.transitions ) ):

			for j in range( len( self.transitions ) ):

				if i == j: 					# do not compare to itself

					continue

				else:						# deterministic TM cannot have transition on same start state and same tape symbol

					if self.transitions[i][ 'startState' ] == self.transitions[j][ 'startState' ]:

						if self.transitions[i][ 'currTapeSymbol' ] == self.transitions[j][ 'currTapeSymbol' ]:

							print( 'Determinism violated at transition: ' + str( self.transitions[i] ) )
							return 0

		return 1

	# PRINT FUNCTIONS

	def printDescription(self):

		return self.printStates() and self.printInputAlphabet() and self.printTapeAlphabet() and self.printTransitions() and self.printStartState() and self.printAccRejState()

	def printInputAlphabet(self):
	
		if len(self.inputAlphabet) == 0:
	
			print('Establish input alphabet via addInputAlphabet().')
			return 0
	
		else:
	
			sys.stdout.write('A:')
	
			for symbol in self.inputAlphabet[:-1]:
	
				sys.stdout.write(symbol)
				sys.stdout.write(',')
	
			sys.stdout.write(self.inputAlphabet[-1])
			sys.stdout.write('\n')
	
			return 1

	def printTapeAlphabet(self):
	
		if len(self.tapeAlphabet) == 0:
	
			print('Establish tape alphabet via addTapeAlphabet().')
			return 0
	
		else:
	
			sys.stdout.write('Z:')
	
			for symbol in self.tapeAlphabet[:-1]:
	
				sys.stdout.write(symbol)
				sys.stdout.write(',')
	
			sys.stdout.write(self.tapeAlphabet[-1])
			sys.stdout.write('\n')
	
			return 1

	def printStates(self):
	
		if len(self.states) == 0:
	
			 print('Establish state list via addStates().')
			 return 0
	
	 	else:
			
			sys.stdout.write('Q:')
		
			for state in self.states[:-1]:
		
				sys.stdout.write(state)
				sys.stdout.write(',')
		
			sys.stdout.write(self.states[-1])
			sys.stdout.write('\n')
		
			return 1

	def printTransitions(self):
		
		if len(self.transitions) == 0:
		
			print('Establish new transition rule via addTransition().')
			return 0
		
		else:
		
			for transition in self.transitions:
	
				sys.stdout.write( 'T:' + transition[ 'startState' ] + ',' + transition[ 'currTapeSymbol' ] + ',' + transition[ 'resultState' ] + ',' )
				sys.stdout.write( transition[ 'writTapeSymbol' ] + ',' + transition[ 'headDirection' ] + '\n')
	
			return 1
		
	def printStartState(self):
	
		if self.startState == "":
	
			print('Establish start state via addStartState().')
			return 0
	
		else:
	
			sys.stdout.write('S:' + self.startState + '\n')
			return 1

	def printAccRejState(self):
	
		if self.acceptState == "" or self.rejectState == "":
	
			print('Establish accept states via addAccRejState().')
			return 0
	
		else:
	
			sys.stdout.write('F:')
	
			sys.stdout.write(self.acceptState + ',')
			sys.stdout.write(self.rejectState)
	
			sys.stdout.write(self.states[-1])
			sys.stdout.write('\n')
			return 1

