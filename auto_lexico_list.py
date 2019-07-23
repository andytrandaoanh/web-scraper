import sys, time 	
import requests
from bs4 import BeautifulSoup
import lxml
import re
from alternate_agent import getRamdomUserAgent
from start_private_proxy import startPrivateProxy
from lexico_list import processLexicoList
from system_handler import writeListToFile, openDir, getFilePath



def getLexico(word, index, proxies, headers):
	DATA_STATUS_OK = 200

	#result = requests.get("https://www.lexico.com/en/definition/" + word)
	

	if (index):
		url =  "https://www.lexico.com/en/list/" + word + '/' + index
	else:
		url =  "https://www.lexico.com/en/list/" + word
	
	response = requests.get(url, proxies=proxies, headers=headers)
	#response = session.get(url, headers=headers)

	if (response.status_code == DATA_STATUS_OK):
		if (response.content):
			try:
				soup = BeautifulSoup(response.content, 'lxml')
				#statusMessage = "Successfully get the word: " + word
							
				#print(data)
				return (str(soup)) 
			except:				
				#statusMessage = "An exception occurred while getting " + word
				return (None)
	

def main(dirOut):
	WORD = "j"
	START_NUMBER = 2 
	STOP_NUMBER	 = 8
	STEP_NUMBER = 1
	
	proxies = startPrivateProxy()
	
	
	for i in range(START_NUMBER, STOP_NUMBER, STEP_NUMBER):	
		print('processing list ', WORD, i)	
		user_agent = getRamdomUserAgent()		
		headers = {'User-Agent': user_agent}
		INDEX = str(i)		 
		pathOut = dirOut + '/list' +  WORD + INDEX + ".txt"
		htmlContent = getLexico(WORD, INDEX, proxies, headers)
		wordData = processLexicoList(htmlContent, WORD)
		writeListToFile(wordData, pathOut)		
		time.sleep(10)

if __name__ == "__main__":

	dirOut = "E:/FULLTEXT/LEXICO/LIST/TEXT"
	main(dirOut)	
	openDir(dirOut)	