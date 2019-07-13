import re


mySpan = """<span class="syn">, scoop up, spade, dig, excavate, move, shift, heap, spoon, ladle, toss</span>"""

myPat = '<span class="phoneticspelling">'



def checkNode(mySpan, myPat):
	pattern = re.compile(myPat)
	match = re.match(pattern, mySpan)
	if (match):
		return True
	else:
		return False



def extractIPA(mySpan):
	items = mySpan.split('/')
	print('/' + items[1] + '/')


def extractWord(mySpan):
	regPat = r'>[\w\s.(),]+<'
	pattern = re.compile(regPat)
	finds = re.findall(pattern, str(mySpan))
	if (finds):
		strOut = finds[0]
		strOut = strOut.replace('>', '')
		strOut = strOut.replace('<', '')
		return(strOut)


print(extractWord(mySpan))
