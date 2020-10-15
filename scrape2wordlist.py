# Filename: 	scrape2wordlist.py
# Author: 		Andrew Afonso
#
# Description: 	A program intended to take in a collection of words (i.e. website scraping)
#				and vary their casing and combination to generate a password wordlist.
#
# Usage:		python scrape2wordlist.py <inputFile.txt> [options]
#
import os
import sys

# Wordlist class
class wordlist:
	def __init__(self):
		self.nums = []
		self.strings = []
		self.specials = []
		self.output = []
		
	def printWL(self):
		print(*self.output, sep="\n")

# Error messages
def error(n):
	if n == 1:
		sys.exit("Not enough arguments (use -h for help).\n")
	if n == 2:
		sys.exit("Mutually exclusive text formatting option specified (use -h for help).\n")
	if n == 3:
		sys.exit("Invalid mixing specifications detected. Likely there is a space in between the brackets somewhere.\n")


# Help message
def help():
	print("-----------")
	print("Basic Usage")
	print("-----------")
	print("python scrape2wordlist.py <inputFile.txt> [options]")
	print("\tJust displays the wordlist in stdout by default.\n")
	print("-o <outputFileName.txt>")
	print("\tSend output to filename specified\n")
	print("-v")
	print("\tDisplays output in stdout even if other options are selected.\n")
	
	print("-----------")
	print("Text Formatting")
	print("-----------")
	print("\tThe program can reformat text strings based on your specifications.")
	print("\tThese arguments will create a seperate item for each reformat.")
	print("\tNOTE: use -Cx, -Ux, -Lx, -LCx to exclude the reformatted string from mixing.\n")
	print("\t-C")
	print("\t\tCapitalize - Capitalize the first character of text strings.")
	print("\t-U")
	print("\t\tUppercase - Convert the entire string to uppercase.")
	print("\t-L")
	print("\t\tLowercase - Convert the entire string to lowercase.")
	print("\t-LC")
	print("\t\tLowercase Capitalized - Convert the entire string to lowercase, then capitalize.")
	
	print("-----------")
	print("Mixing")
	print("-----------")
	print("\tThe program can combine elements based on your specifications\n")
	print("General form: -<mix code> [spec1, spec2, spec3, etc]\n")
	print("-- Mix Codes\n")
	print("\t-mN [specifications]")
	print("\t\tMix numbers.")
	print("\t\t- This will mix strings that satisfy the function int(line) based on the supplied specifications\n")
	print("\t-mS [specifications]")
	print("\t\tMix strings.")
	print("\t\t- This will mix in text strings based on the supplied specifications\n")
	
	print("-- Specification Format:")
	print("\tFor each mixing type, you need to specify additional arguments to control the combination format.")
	print("\tPlace arguement values in brackets following the mix code, using commas to seperate each specification,")
	print("\tand brackets to surround them.")
	print("\tEx: -mS [mi=3,ma=7,f,b]  - NO SPACES IN BETWEEN\n")
	print("\tmi=#")
	print("\t\tMinimum Length - Only use strings at least # characters long\n")
	print("\tma=#")
	print("\t\tMaximum Length - Only use strings at most # characters long\n")
	print("\tf")
	print("\t\tFront Mixing - Combine values at the beginning (mixitem) + (line)\n")
	print("\tb")
	print("\t\tBack Mixing - Append the values to the end (line) + (mixitem)\n")
	
	print("-----------")
	print("Examples")
	print("-----------")
	print("\tpython scrape2wordlist.py infile.txt -C -Ux -v -mN [f,b] -o newwordlist.txt\n")
	print("\t\tFor input line \"clEveland\", the following lines will be outputted, and stored in newwordlist.txt:")
	print("\t\t\tclEveland")
	print("\t\t\tclEveland1")
	print("\t\t\tclEveland123")
	print("\t\t\t1clEveland")
	print("\t\t\t123clEveland")
	print("\t\t\tClEveland")
	print("\t\t\tClEveland1")
	print("\t\t\tClEveland123")
	print("\t\t\t1ClEveland")
	print("\t\t\t123ClEveland")
	print("\t\t\tCLEVELAND")
	sys.exit()

# String shuffling
def shuffleStrings(wordlist, arguments):
	mi = 0
	ma = 0
	newStrings = []
	# Set the mi or ma values if they are specified
	for item in arguments:
		if "=" in item:
			temp = item.split("=")
			if temp[0] == "mi":
				mi = int(temp[1])
				arguments[arguments.index(item)] = "mi"
			if temp[0] == "ma":
				ma = int(temp[1])
				arguments[arguments.index(item)] = "ma"
				
	for baseWord in wordlist.strings:
		for mixWord in wordlist.strings:
			status = 1
			if "mi" in arguments:
				if len(mixWord) < mi:
					status = 0
			if "ma" in arguments:
				if len(mixWord) > ma:
					status = 0
			if status == 1:
				if "b" in arguments:
					newWord = baseWord + mixWord
					newStrings.append(newWord)
				if "f" in arguments:
					newWord =  mixWord + baseWord
					newStrings.append(newWord)
	wordlist.strings = wordlist.strings + newStrings
	wordlist.output = wordlist.output + newStrings
	return

# Number shuffling
def shuffleNumbers(wordlist, arguments):
	mi = 0
	ma = 0
	newStrings = []
	# Set the mi or ma values if they are specified
	for item in arguments:
		if "=" in item:
			temp = item.split("=")
			if temp[0] == "mi":
				mi = int(temp[1])
				arguments[arguments.index(item)] = "mi"
			if temp[0] == "ma":
				ma = int(temp[1])
				arguments[arguments.index(item)] = "ma"
				
	for baseWord in wordlist.strings:
		for mixNum in wordlist.nums:
			status = 1
			if "mi" in arguments:
				if len(str(mixNum)) < mi:
					status = 0
			if "ma" in arguments:
				if len(str(mixNum)) > ma:
					status = 0
			if status == 1:
				if "b" in arguments:
					newWord = baseWord + str(mixNum)
					newStrings.append(newWord)
				if "f" in arguments:
					newWord =  str(mixNum) + baseWord
					newStrings.append(newWord)
	wordlist.strings = wordlist.strings + newStrings
	wordlist.output = wordlist.output + newStrings
	return

# Output to file
def writeOut(wordlist, outputFileName):
	with open(outputFileName, 'a+') as outFile:
		for line in wordlist.output:
			outFile.write(line + "\n")


def main():
	if len(sys.argv) < 2:
		error(1)
	if "-h" in sys.argv:
		help()
	if "-U" in sys.argv and "-Ux" in sys.argv:
		error(2)
	if "-C" in sys.argv and "-Cx" in sys.argv:
		error(2)
	if "-L" in sys.argv and "-Lx" in sys.argv:
		error(2)
	if "-LC" in sys.argv and "-LCx" in sys.argv:
		error(2)
		
	inFilePath = sys.argv[1]
	inputFile = open(inFilePath, 'r')
	inputContents = set(inputFile.readlines())
	newWordlist = wordlist()
	
	for line in inputContents:
		line = line.strip()
		newWordlist.output.append(line)
		try:
			newint = int(line)
			if "-mN" in sys.argv:
				newWordlist.nums.append(newint)
		except ValueError:
			newWordlist.strings.append(line)
			if "-U" in sys.argv and line.upper() != line:
				newWordlist.strings.append(line.upper())
				newWordlist.output.append(line.upper())
			if "-Ux" in sys.argv and line.upper() != line:
				newWordlist.output.append(line.upper())
			if "-L" in sys.argv and line.lower() != line:
				newWordlist.strings.append(line.lower())
				newWordlist.output.append(line.lower())
			if "-Lx" in sys.argv and line.lower() != line:
				newWordlist.output.append(line.lower())
			if "-C" in sys.argv and line.capitalize() != line:
				newWordlist.strings.append(line.capitalize())
				newWordlist.output.append(line.capitalize())
			if "-Cx" in sys.argv and line.capitalize() != line:
				newWordlist.output.append(line.capitalize())
			if "-LC" in sys.argv and (line.lower()).capitalize() != line:
				newWordlist.strings.append((line.lower()).capitalize())
				newWordlist.output.append((line.lower()).capitalize())
			if "-LCx" in sys.argv and (line.lower()).capitalize() != line:
				newWordlist.output.append((line.lower()).capitalize())
					
	if "-mS" in sys.argv:
		if "]" not in sys.argv[sys.argv.index("-mS") + 1]:
			error(3)
		else:
			shuffleStrings(newWordlist, (sys.argv[sys.argv.index("-mS") + 1].replace("[","").replace("]","")).split(","))
			
	if "-mN" in sys.argv:
		if "]" not in sys.argv[sys.argv.index("-mN") + 1]:
			error(3)
		else:
			shuffleNumbers(newWordlist, (sys.argv[sys.argv.index("-mN") + 1].replace("[","").replace("]","")).split(","))
	
	if not "-o" in sys.argv or "-v" in sys.argv:
		newWordlist.printWL()
		
	if "-o" in sys.argv:
		writeOut(newWordlist, sys.argv[sys.argv.index("-o") + 1])
	
	sys.exit()
	
if __name__ == "__main__":
    main()
