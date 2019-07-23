import re
from bs4 import BeautifulSoup
import lxml
from system_handler import writeListToFile, openDir, getFilePath



def processLexicoList(contents, word):
	soup = BeautifulSoup(contents, "lxml")
	itemList = soup.find_all('a', href=True, text=True)
	
	itemData = []

	for item in itemList:
		hrefText = str(item['href'])
		if ('/en/definition/' + word) in hrefText:
			#print(item.get_text(), '\n')
			itemData.append(item.get_text())
	return itemData	


	




	

if __name__ == "__main__":

	WORD = "k"
	INDEX = ""
	dirOut = "E:/FULLTEXT/LEXICO/LIST/TEXT"
	pathIn = "E:/FULLTEXT/LEXICO/LIST/HTML/List" + WORD + INDEX + ".html"
	pathOut = getFilePath(pathIn, dirOut)
	
	#print(pathOut)
	
	wordData =[]

	with open(pathIn, "r", encoding="utf-8") as file:
		contents = file.read()
		wordData = processLexicoList(contents, WORD)
	
	
	writeListToFile(wordData, pathOut)
	openDir(dirOut)

		
