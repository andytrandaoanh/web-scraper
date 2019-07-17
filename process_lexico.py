import re
from bs4 import BeautifulSoup
import lxml


def hasNumber(sInput):
	return bool(re.search(r'\d', sInput))
def extractHW(sInput):
	sNum = re.findall(r'\d+', sInput)
	idx =  sNum[0]
	sWord = sInput.split(idx)[0]
	return(sWord, idx)



def processLexico(contents):
	soup = BeautifulSoup(contents, "lxml")
	#hw = soup.find("span", {"class" : "hw"})
			
	#if hasNumber(hw.text):
	#	headWord, index = extractHW(hw.text)
	#	print("head word:", headWord, "index", index)
	#else:
	#	print("head word has no number")

	#output: a1	

	#hwList = soup.find_all("span", {"class" : "hw"})
	#print('number of head words:', len(hwList))
	#output: 4

	#span =  hwList[0].find_next('span', {"class" : "pos"})
	
	#print(span, '\n')
	sections = soup.find_all("section")
	for sect in sections:
		print(sect, '\n')



if __name__ == "__main__":
	pathIn = "E:/FULLTEXT/LEXICO/a.html"
	with open(pathIn, "r", encoding="utf-8") as file:
		contents = file.read()
		processLexico(contents)
		
