# scrape2wordlist
A program for taking pre-existing wordlists (maybe one scraped from a website), and generating a new wordlist based on that.

## Help text (-h)
-----------
Basic Usage
-----------
python scrape2wordlist.py <inputFile.txt> [options]
	Just displays the wordlist in stdout by default.

-o <outputFileName.txt>
	Send output to filename specified

-v
	Displays output in stdout even if other options are selected.

-----------
Text Formatting
-----------
	The program can reformat text strings based on your specifications.
	These arguments will create a seperate item for each reformat.
	NOTE: use -Cx, -Ux, -Lx, -LCx to exclude the reformatted string from mixing.

	-C
		Capitalize - Capitalize the first character of text strings.
	-U
		Uppercase - Convert the entire string to uppercase.
	-L
		Lowercase - Convert the entire string to lowercase.
	-LC
		Lowercase Capitalized - Convert the entire string to lowercase, then capitalize.
-----------
Mixing
-----------
	The program can combine elements based on your specifications

General form: -<mix code> [spec1, spec2, spec3, etc]

-- Mix Codes

	-mN [specifications]
		Mix numbers.
		- This will mix strings that satisfy the function int(line) based on the supplied specifications

	-mS [specifications]
		Mix strings.
		- This will mix in text strings based on the supplied specifications

-- Specification Format:
	For each mixing type, you need to specify additional arguments to control the combination format.
	Place arguement values in brackets following the mix code, using commas to seperate each specification,
	and brackets to surround them.
	Ex: -mS [mi=3,ma=7,f,b]  - NO SPACES IN BETWEEN

	mi=#
		Minimum Length - Only use strings at least # characters long

	ma=#
		Maximum Length - Only use strings at most # characters long

	f
		Front Mixing - Combine values at the beginning (mixitem) + (line)

	b
		Back Mixing - Append the values to the end (line) + (mixitem)

-----------
Examples
-----------
	python scrape2wordlist.py infile.txt -C -Ux -v -mN [f,b] -o newwordlist.txt

		For input line "clEveland", the following lines will be outputted, and stored in newwordlist.txt:
			clEveland
			clEveland1
			clEveland123
			1clEveland
			123clEveland
			ClEveland
			ClEveland1
			ClEveland123
			1ClEveland
			123ClEveland
			CLEVELAND
