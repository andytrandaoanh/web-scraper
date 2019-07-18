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
	
	#step 1: retrieve all word heads
	#each word head will form an entry
	#hwList = soup.find_all("span", {"class" : "hw"})
	
	#first word head parent
	#parents = hwList[0].parents
	#for parent in parents:
	#	print(parent, '\n')		
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
	#sections = soup.find_all("section")
	#for sect in sections:
	#	print(sect, '\n')


	#h2 <h2 class="hwg"><span class="hw" data-headword-id="a">
	#entries = soup.find_all("h2", {"class" : "hwg"})	
	#for entry in entries:
	#	print(entry, '\n')
	#firstH2 = entries[0]
	#children = firstH2.children
	#for child in children:
	#	print(child, '\n')

	# try to understand pos
	# span class="pos">determiner</span>
	# parent is <h3 class="ps pos"><span class="pos">determiner</span></h3> 

	#pos_spans = soup.find_all("span", {"class" : "pos"})	
	#for span in pos_spans:
	#	print(span.parent, '\n')	

	#h3 <h2 class="hwg"><span class="hw" data-headword-id="a">
	#entries = soup.find_all("h3", {"class" : "ps pos"})	
	#for entry in entries:
	#	print(entry, '\n')
	#firstH2 = entries[0]
	#children = firstH2.children
	#for child in children:
	#	print(child, '\n')	

	hwList = soup.find_all("span", {"class" : "hw"})
	categories = hwList[0].find_next_all("h3", {"class" : "ps pos"})
	print(categories)

if __name__ == "__main__":
	pathIn = "E:/FULLTEXT/LEXICO/a.html"
	with open(pathIn, "r", encoding="utf-8") as file:
		contents = file.read()
		processLexico(contents)
		
