import requests
from bs4 import BeautifulSoup
import lxml
import re
from system_handler import writeJSON, openDir
from get_mp3 import getAudio
from tor import getSafeSession
from process_lexico_2 import processPage




def getLexico(word, session, headers):

	#result = requests.get("https://www.lexico.com/en/definition/" + word)
	url =  "https://dictionary.cambridge.org/dictionary/english/" + word
	result = session.get(url, headers=headers)


	src = result.content

	soup = BeautifulSoup(src, 'lxml')

	print(soup.prettify())


	#scans = soup.find_all(["span", "strong", {"class": "syn"}, "p"])

	#print(scans)

	#wordObject = processPage(scans)

	#return(wordObject)


if __name__ == "__main__":

	WORD = "man"
	dirOut = "E:/FULLTEXT/LEXICO" 
	pathOut = dirOut + '/' +  WORD + ".json"
	session, headers = getSafeSession()
	#print('session', session)
	#print('headers', headers)
	wordObject = getLexico(WORD, session, headers)
	#print(wordObject)
	#writeJSON(wordObject, pathOut)
	#openDir(dirOut)
	