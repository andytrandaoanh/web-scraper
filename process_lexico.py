import re
from bs4 import BeautifulSoup
import lxml
from system_handler import writeListToFile, openDir, getFilePath


def hasNumber(sInput):
	return bool(re.search(r'\d', sInput))

def extractHW(sInput):
	sOutput = ''
	if (hasNumber(sInput)):
		sOutput = re.sub(r'\d', '', sInput)
	else:
		sOutput = sInput.strip()
	return sOutput


def processSpan(item):
	#spanString = str(item)
	#spanText = item.get_text()
	span = ''
	if item.has_attr('class'):
		className = item['class'][0] 
		if(className == 'hw'):
			if(item.get_text().strip()):
				span = '[head-word]' + extractHW(item.get_text())
		elif(className == 'phoneticspelling'):
			if(item.get_text().strip()):
				span = '[phonetic]' + item.get_text()
		elif(className == 'pos'):
			if(item.get_text().strip()):
				span = '[category]' + item.get_text()
		elif(className == 'iteration'):
			if(item.get_text().strip()):
				span = '[senseno]' + item.get_text()
		elif(className == 'subsenseIteration'):
			if(item.get_text().strip()):
				span = '[senseno]' + item.get_text()		
		elif(className == 'inflection-text'):
			if(item.get_text().strip()):
				span = '[inflection]' + item.get_text()
		elif(className == 'grammatical_note'):
			if(item.get_text().strip()):
				span = '[grammar]' + item.get_text()
		elif(className == 'sense-registers'):
			if(item.get_text().strip()):
				span = '[grammar]' + item.get_text()
		elif(className == 'sense-regions'):
			if(item.get_text().strip()):
				span = '[grammar]' + item.get_text()				
		elif(className == 'ind'):
			if(item.get_text().strip()):
				span = '[meaning]' + item.get_text()


	return span

def processDiv(item):
	divData = []

	if item.has_attr('class'):
		className = item['class'][0] 
		if(className == 'variant'):
			div = '[variant]' + item.get_text()
			divData.append(div)
		elif (className == 'senseInnerWrapper'):
			if item.parent.has_attr('class'):
				parentClass = item.parent['class'][0]
				if (parentClass == 'etymology'):
					textH3 = item.parent.find('h3').get_text()
					textP = item.find('p').get_text()
					if (textH3 == 'Usage'):						
						div = '[usage]' + textP
						divData.append(div)
					elif (textH3 == 'Origin'):
						div = '[origin]' + textP
						divData.append(div)
					elif (textH3 == 'Phrases'):
						div = '[phrases]'
						divData.append(div)
						phrase = item.find('strong', {'class': 'phrase'})
						phraseText = phrase.get_text()
						if(phraseText):
							divData.append('[phrase]' + phraseText)


					
	return divData


def processEm(item):
	em = ''
	
	if item.parent.has_attr('class'):
		parentClass = item.parent['class'][0]
		if (parentClass == 'ex'):
			itemText = item.get_text()
			if(itemText):
				em = '[example]' + itemText.strip()		
	
	return(em)



	


def processLexico(contents):
	soup = BeautifulSoup(contents, "lxml")
	itemList = soup.find_all(['span', 'em', 'div'])
	
	itemData = []

	for item in itemList:
		if (item.name == 'span'):
			wordSpan = processSpan(item)
			if(wordSpan):
				itemData.append(wordSpan)
		elif (item.name == 'em'):
			wordEm = processEm(item)
			if(wordEm):
				itemData.append(wordEm)
		elif (item.name == 'div'):
			wordDivs = processDiv(item)
			if(wordDivs):
				for wordDiv in wordDivs:
					itemData.append(wordDiv)

	return itemData

	#entryList = soup.find_all('div', {'class' : 'entryWrapper'})
	#print(len(entryList))
	#for item in entryList:
	#	print(item)

	




	

if __name__ == "__main__":

	WORD = "at"
	dirOut = "E:/FULLTEXT/LEXICO/TEXT"
	pathIn = "E:/FULLTEXT/LEXICO/HTML/" + WORD + ".html"
	pathOut = getFilePath(pathIn, dirOut)
	
	#print(pathOut)
	
	wordData =[]

	with open(pathIn, "r", encoding="utf-8") as file:
		contents = file.read()
		wordData = processLexico(contents)
	
	
	writeListToFile(wordData, pathOut)
	openDir(dirOut)

		
