import requests
from bs4 import BeautifulSoup
import lxml
import re
from system_handler import writeJSON, openDir



def extractWord(mySpan):
	regPat = r'>[\w\s.(),]+<'
	pattern = re.compile(regPat)
	finds = re.findall(pattern, str(mySpan))
	if (finds):
		strOut = str(finds[0])
		strOut = strOut.replace('>', '')
		strOut = strOut.replace('<', '')
		return(strOut)


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


def getLexico(word):

	result = requests.get("https://www.lexico.com/en/definition/" + word)
	src = result.content

	soup = BeautifulSoup(src, 'lxml')

	spans = soup.find_all("span")

	wordObject = {
		'word': None,
		'meaning': [],
		'phonetic': None
	}





	for span in spans:
		meaningObj = {
			'category': None,
			'definition': [],
			'synonym': [],
			'inflection': []
		}
		if (checkNode(span, r'<span class="hw"')):
			wordObject['word'] = extractWord(span)
		if (checkNode(span, r'<span class="pos">')):			
			meaningObj['category'] = extractWord(span)
			wordObject['meaning'].append(meaningObj)
		if (checkNode(span, r'<span class="ind">')):
			wordObject['meaning'][-1]['definition'].append(extractWord(span))
		if (checkNode(span, r'<span class="inflection-text">')):
			wordObject['meaning'][-1]['inflection'].append(extractWord(span).replace(",", "").strip())
		if (checkNode(span, r'<span class="syn">')):
			syn = extractWord(span)
			if(syn):
				wordObject['meaning'][-1]['synonym'].append(syn.replace(',', '').strip())
			
		if (checkNode(span, r'<span class="phoneticspelling">')):
			wordObject['phonetic'] = extractIPA(span)
	return(wordObject)


if __name__ == "__main__":

	WORD = "dance"
	dirOut = "E:/FULLTEXT/LEXICO" 
	pathOut = dirOut + '/' +  WORD + ".json"
	wordObject = getLexico(WORD)
	writeJSON(wordObject, pathOut)
	openDir(dirOut)
	