import re


mySpan = """<strong class="phrase">come amid</strong>"""

myPat = 'span class="hw"'

def extractStrong(myStrong):
	inputText = str(myStrong)
	regPat = r'<strong class="[\w\-\s]+">[\w\s,().]+'
	pattern = re.compile(regPat)
	finds = re.findall(pattern, inputText)
	if(finds):
		find = finds[0]
		temp = find.split(">")
		return(str(temp[1]))



def extractContent(mySpan):
	inputText = str(mySpan)
	regPat = r'<span class="[\w\-\s]+">[\w]+'
	pattern = re.compile(regPat)
	finds = re.findall(pattern, inputText)
	if(finds):
		find = finds[0]
		temp = find.split(">")
		return(temp[1])

def extractP(myP):
	inputText = str(myP)
	outText = inputText.replace('<p>', '')
	outText = outText.replace('</p>', '')
	return str(outText)


cont = extractStrong(mySpan)
print(cont)

