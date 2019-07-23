import requests
from bs4 import BeautifulSoup
import lxml
import re
from system_handler import writeJSON, openDir
from alternate_agent import getRamdomUserAgent
from start_private_proxy import startPrivateProxy




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
	



if __name__ == "__main__":

	WORD = "k"
	INDEX = ""
	dirOut = "E:/FULLTEXT/LEXICO/LIST/HTML" 
	pathOut = dirOut + '/list' +  WORD + INDEX + ".html"

	proxies = startPrivateProxy()

	user_agent = getRamdomUserAgent()		
	headers = {'User-Agent': user_agent}


	
	
	htmlContent = getLexico(WORD, INDEX, proxies, headers)
	if(htmlContent):
		with open(pathOut, "w", encoding='utf-8') as file:
			file.write(htmlContent)
	openDir(dirOut)
	