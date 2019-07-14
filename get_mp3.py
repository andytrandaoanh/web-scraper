
import wget
from system_handler import getFilePath, openDir


def getAudio(audioList):
	

	temp = str(audioList[0])
	items = temp.split('src=')
	temp = items[1].split("><")
	url = temp[0]
	print('url', url)
	#myFile = getFilePath(url)

	print("starting downloading ", url, "...")

	#dirOut = "E:/FULLTEXT/LEXICON/AUDIO/" 

	#pathOut = dirOut + myFile

	file = wget.download(url)


	print("finished downloading ", file)


	
