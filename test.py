import re

def hasNumber(sInput):
	return bool(re.search(r'\d', sInput))

def extractHW(sInput):
	sWord = ''
	sNumber = ''
	if (hasNumber(sInput)):
		sWord = re.sub(r'\d', '', sInput)
		if(sWord):
			temps = sInput.split(sWord)
			sNumber = temps[1]
	else:
		sWord = sInput.strip()
	return sWord, sNumber


sInput = "head15"

print(extractHW(sInput))