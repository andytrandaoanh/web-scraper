import re


mySpan = """<span class="ind">A nocturnal badger-sized burrowing mammal of Africa, with long ears, a tubular snout, 
and a long extensible tongue, feeding on ants and termites.</span>"""

myPat = '<span class="ind">'



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


def extractWord(mySpan, myPat):
	inputString = str(mySpan)
	pattern = re.compile(myPat)
	matchObj = re.match(pattern, inputString)
	if(matchObj):
		temp = mySpan.split(myPat)
		myCont = temp[1].replace('\n', '')
		myCont = myCont.replace('</span>', '')
		return myCont
	
	#temp = str(mySpan).split(startSpan)
	#pattern = re.compile(startSpan)
	
	#print(matchObj)
	


print(extractWord(mySpan, myPat))
