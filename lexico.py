import sys, time 	
import requests, json
import system_handler as sysHand
from alternate_agent import getRamdomUserAgent
from start_private_proxy import startPrivateProxy
from bs4 import BeautifulSoup
import lxml
from system_handler import getLineFromTextFile



class ProxyEngine:

	def __init__(self, pathProxy): 
		self.pathProxy = pathProxy		
		self.curIndex = 0
		self.proxyList = []
		

	def loadData(self):
		temp = getLineFromTextFile(self.pathProxy)
		self.proxyList = [item for item in temp if item]
		#print(self.proxyList)

	def nextProxy(self):
		#print('current index:', self.curIndex)
		if self.curIndex < len(self.proxyList):
			currentProxy = self.proxyList[self.curIndex]
			self.curIndex +=1
			proxyOut = {}
			proxyOut['http'] = currentProxy
			proxyOut['https'] = currentProxy
			return(proxyOut)
			

		else:
			self.curIndex = 0


class DictEngine:

	def __init__(self, pathDict, startIndex=0): 
		self.pathDict = pathDict		
		self.curIndex = startIndex
		self.DictList = []
		

	def loadData(self):
		temp = getLineFromTextFile(self.pathDict)
		self.DictList = [item for item in temp if item]
		#print(self.DictList)

	def nextWord(self):
		#print('current index:', self.curIndex)
		if self.curIndex < len(self.DictList):
			currentWord = self.DictList[self.curIndex]
			self.curIndex +=1
			return(currentWord)



def getSingleWord(wordIn, proxies, headers):
	
	DATA_STATUS_OK = 200

	apiCompatibleWord = wordIn.replace(' ' , '_').lower()
	apiCompatibleWord = apiCompatibleWord .replace('/' , '%')


	url =  "https://www.lexico.com/en/definition/" + apiCompatibleWord

	response = requests.get(url, proxies=proxies, headers=headers)


	if (response.status_code == DATA_STATUS_OK):
		if (response.content):
			try:
				soup = BeautifulSoup(response.content, 'lxml')
				data = str(soup)
				statusMessage = "Successfully get the word: " + wordIn + "=>" + apiCompatibleWord
				return (data, statusMessage) 
			except:				
				statusMessage = "An exception occurred while getting "  + wordIn + "=>" + apiCompatibleWord
				return (None, statusMessage)

	else:		
		statusMessage = "Fail to remotely get the word " + word
		return (None, statusMessage)



def runDownLoad(START_NUMBER, proxies, headers, mode, location):
	
	PATH_IN = "E:/FULLTEXT/DICTIONARY/NORMALCASE/Combined Lexico Oxford.txt"

	
	DIR_DATA_OUT = ''
	DIR_LOG_OUT = ''


	print('Path In:', PATH_IN)
	#For Home only

	if (mode == "local"):
		DIR_DATA_OUT = "E:/FULLTEXT/LEXICO/HTML"
		DIR_LOG_OUT = "E:/FULLTEXT/LEXICO/LOG"
	
	elif (mode == "remote"):
		if (location == "home"):
			DIR_DATA_OUT = "C:/Users/Andy Anh/Dropbox/PROGRAMMING/FULLTEXT/LEXICO/HTML"
			DIR_LOG_OUT = "C:/Users/Andy Anh/Dropbox/PROGRAMMING/FULLTEXT/LEXICO/LOG"
		elif (location == "office"): 
			DIR_DATA_OUT = "C:/Users/Administrator/Dropbox/PROGRAMMING/FULLTEXT/LEXICO/HTML"
			DIR_LOG_OUT = "C:/Users/Administrator/Dropbox/PROGRAMMING/FULLTEXT/LEXICO/LOG"

	print('\nData Path:', DIR_DATA_OUT, '\nLog Path:', DIR_LOG_OUT)



	STOP_NUMBER = START_NUMBER + 10

	print('starting at:', START_NUMBER)
	print('using agent:', headers['User-Agent'])

	#NOTE: LOG IS FOR EVERY BATCH
	#pathDataOut, pathStatusOut = sysHand.getIncrementPath(START_NUMBER, PATH_DATA_OUT, PATH_LOG_OUT)
	pathStatusOut = sysHand.getIncrementLogPath(START_NUMBER, DIR_LOG_OUT)

	wordList = sysHand.getLineFromTextFile(PATH_IN)
	
	#results = []
	status = []
	dateStamp = sysHand.getDateStamp()
	status.append('Starting scraping Lexico at  ' + dateStamp)
	status.append('Starting scraping at index ' + str(START_NUMBER))
	status.append('Starting scraping using IP ' + proxies['http'])
	status.append('Starting scraping using agent ' + headers['User-Agent'])



	for i in range(START_NUMBER, STOP_NUMBER):
		pathDataOut = sysHand.getIncrementDataPath(i, DIR_DATA_OUT)
		word = wordList[i]
		(htmlData, message) = getSingleWord(word, proxies, headers)
		if(htmlData):
			with open(pathDataOut, "w", encoding='utf-8') as file:
				file.write(htmlData)
		print(i, ':',  message)
		status.append(str(i) + ' ' + message)
		time.sleep(5)

	#sysHand.writeDataToJSON(results, pathDataOut)
	dateStamp = sysHand.getDateStamp()
	status.append('Ending scraping Lexico at ' + dateStamp)
	sysHand.writeListToFile(status, pathStatusOut)

def startLoop(startNumber, mode, location):
	#START_NUMBER = 107200
	START_NUMBER = startNumber 
	STOP_NUMBER	 = START_NUMBER + 10000
	STEP_NUMBER = 10

	#pathList = 'D:/Proxy/List/raw_text_rudnkh.txt'
	#pathList = 'D:/Proxy/List/raw_text_clarketm.txt'
	

	#PATH TO PROXY LIST
	#pathList = 'D:/Proxy/Filter/good_proxy_list.txt'
	pathList = 'D:/Proxy/List/raw_list_general.txt'
	myProxy  = ProxyEngine (pathList)
	myProxy.loadData()


	pathDict = 'E:/FULLTEXT/DICTIONARY/LOWERCASE/NLTK_Dictionary.txt'

	myDict = DictEngine(pathDict, START_NUMBER)
	myDict.loadData()





	for i in range(START_NUMBER, STOP_NUMBER, STEP_NUMBER):		
		user_agent = getRamdomUserAgent()		
		headers = {'User-Agent': user_agent}
		proxies = {}
		proxyOK = False
		while not proxyOK:
			try:
				proxies = myProxy.nextProxy()
				badIP = proxies['http']
				print('Attemping on', badIP, '...')
				urlTest = "http://icanhazip.com"
				resTest = requests.get(urlTest, proxies=proxies, headers=headers)
				#print('using IP:', resTest.text)
				proxyOK = True
			except Exception as e:
				print('Test failed on icanhazip.com')

		if proxies:
			print(proxies)
			nextWord = myDict.nextWord()
			print('nextWord', nextWord)

			#url = 'https://www.dictionary.com/browse/' + nextWord
			#https://dictionary.cambridge.org/dictionary/english/fancy

			url = 'https://dictionary.cambridge.org/dictionary/english/' + nextWord


			try:
				response = requests.get(url, proxies=proxies, headers=headers)
				if response.status_code == 200:
					pathLog = 'D:/Proxy/Filter/good_proxy_list.txt'
					goodIP = proxies['http']
					print('Discoved good proxy:', goodIP)
					with open(pathLog, "a") as myfile:
						myfile.write(goodIP + '\n')


			except Exception as e:
				#print (e)
				print('Test failed on dictionary.cambridge.org')
			
			#runDownLoad(i, proxies, headers, mode, location)
			time.sleep(3)


if __name__ == '__main__':

	startNumber = 4700
	startLoop(startNumber, 'local', 'office')

