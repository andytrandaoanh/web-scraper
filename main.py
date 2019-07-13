import requests
from bs4 import BeautifulSoup
import lxml
import re
from system_handler import writeJSON, openDir



def extractWord(mySpan, myPat):
	inputString = str(mySpan)
	pattern = re.compile(myPat)
	matchObj = re.match(pattern, inputString)
	if(matchObj):
		temp = inputString.split(">")
		myCont = temp[1].replace('\n', '')
		myCont = myCont.replace('</span', '')
		return myCont
	


def extractIPA(mySpan):
	items = str(mySpan).split('/')
	return('/' + items[1] + '/')

def checkNode(mySpan, myPat):
	pattern = re.compile(myPat)
	match = re.match(pattern, str(mySpan))
	if (match):
		return True
	else:
		return False

def getOrigin(divs):
	origin = ''
	for div in divs:
		if (checkNode(div, r'<div class="senseInnerWrapper">')):
			ps = str(div).split("<p>")
			if(ps[1]):
				tempOrigin = ps[1].split("</p>")
				if(tempOrigin[0]):
					origin = tempOrigin[0]					
					
	return (str(origin))

def getLexico(word):

	result = requests.get("https://www.lexico.com/en/definition/" + word)
	src = result.content

	soup = BeautifulSoup(src, 'lxml')

	spans = soup.find_all("span")

	#print(spans)
	



	wordObject = {
		'word': None,
		'meaning': [],
		'phonetic': None,
		'origin': None
	}





	for span in spans:
		meaningObj = {
			'category': None,
			'definition': [],
			'synonym': [],
			'inflection': []
		}
		if (checkNode(span, r'<span class="hw"')):
			wordObject['word'] = extractWord(span, '<span class="hw"')
		if (checkNode(span, r'<span class="pos">')):			
			meaningObj['category'] = extractWord(span, '<span class="pos">')
			wordObject['meaning'].append(meaningObj)
		if (checkNode(span, r'<span class="ind">')):
			wordObject['meaning'][-1]['definition'].append(extractWord(span, '<span class="ind">'))
		if (checkNode(span, r'<span class="inflection-text">')):
			wordObject['meaning'][-1]['inflection'].append(extractWord(span, '<span class="inflection-text">').replace(",", "").strip())
		if (checkNode(span, r'<span class="syn">')):
			syn = extractWord(span, '<span class="syn">')
			if(syn):
				wordObject['meaning'][-1]['synonym'].append(syn.replace(',', '').strip())
			
		if (checkNode(span, r'<span class="phoneticspelling">')):
			wordObject['phonetic'] = extractIPA(span)

	divs = soup.find_all("div")
	origin = getOrigin(divs)
	wordObject['origin'] = origin


	return(wordObject)


if __name__ == "__main__":

	WORD = "aardvark"
	dirOut = "E:/FULLTEXT/LEXICO" 
	pathOut = dirOut + '/' +  WORD + ".json"
	wordObject = getLexico(WORD)
	#print(wordObject)
	writeJSON(wordObject, pathOut)
	openDir(dirOut)
	