import re

spans = [
'<span class="hw" data-headword-id="family">family</span>', 

'<span class="pos">noun</span>', 

'<span class="inflection-text">families</span>', 

'<span class="iteration">1</span>' ,

'<span class="grammatical_note">treated as singular or plural</span>' ,

'<span class="ind">A group consisting of two parents and their children living together as a unit.</span>', 

'<span class="grammatical_note">as modifier</span>', 

'<span class="syn">, ménage</span>',

'<span class="subsenseIteration">1.1</span>', 

'<span class="ind">A group of people related by blood or marriage.</span>', 

"""<span class="syn">, relations, blood relations, family members, kin, next of kin, kinsfolk, kinsmen, kinswomen, kindred, one's flesh and blood, one's own flesh and blood, connections</span>""",

'<span class="subsenseIteration">1.2</span>', 

'<span class="ind">The children of a person or couple being discussed.</span>', 

'<span class="syn">, little ones, youngsters</span>', 

'<span class="subsenseIteration">1.3</span>', 

'<span class="sense-registers">informal </span>', 

'<span class="ind">A local organizational unit of the Mafia or other large criminal group.</span>', 

'<span class="iteration">2</span>', 

'<span class="ind">All the descendants of a common ancestor.</span>', 


'<span class="syn">, parentage, birth, pedigree, genealogy, background, family tree, descent, lineage, line, line of descent, bloodline, blood, extraction, derivation, race, strain, stock, breed</span>',

'<span class="subsenseIteration">2.1</span>', 

'<span class="ind">A group of peoples from a common stock.</span>', 

'<span class="syn">, stock, strain, line, family</span>', 

'<span class="iteration">3</span>', 

'<span class="ind">A group of related things.</span>', 


'<span class="subsenseIteration">3.1</span>', 

'<span class="sense-regions domain_labels">Biology </span>', 

'<span class="ind">A principal taxonomic category that ranks above genus and below order, usually ending in -idae (in zoology) or -aceae (in botany)</span>', 

'<span class="syn">, group, order, class, subclass, genus, species</span>', 

'<span class="subsenseIteration">3.2</span>',

'<span class="ind">All the languages ultimately derived from a particular early language, regarded as a group.</span>', 

'<span class="subsenseIteration">3.3</span>', 

'<span class="sense-regions domain_labels">Mathematics </span>', 

'<span class="ind">A group of curves or surfaces obtained by varying the value of a constant in the equation generating them.</span>', 

'<span class="pos">adjective</span>', 

'<span class="grammatical_note">attributive</span>', 

'<span class="iteration"></span>', 

'<span class="ind">Designed to be suitable for children as well as adults.</span>', 

'<span class="sense-registers">informal </span>' 

'<span class="iteration"></span>', 

'<span class="ind">Pregnant.</span>' ,

'<span class="iteration"></span>' ,

'<span class="ind">Part with a valuable resource for immediate advantage.</span>' ,

'<span class="phoneticspelling">/ˈfamɪli/</span>' ,

'<span class="phoneticspelling">/ˈfam(ə)li/</span>',


]


def extractIPA(mySpan):
	items = str(mySpan).split('/')
	return('/' + items[1] + '/')

def extractContent(mySpan):
	inputText = str(mySpan)
	regPat = r'<span class="[\w\-\s]+">[\w\s,().]+'
	pattern = re.compile(regPat)
	finds = re.findall(pattern, inputText)
	if(finds):
		find = finds[0]
		temp = find.split(">")
		return(temp[1])

def extractHeadWord(mySpan):
	inputText = str(mySpan)
	regPat = r'<span class="hw" data-headword-id="[\w]+'
	pattern = re.compile(regPat)
	finds = re.findall(pattern, inputText)
	if(finds):
		find = finds[0]
		temps = find.split('<span class="hw" data-headword-id="')
		return(temps[1])	


def processPage(spanList):
	wordObject = {
	'word': None,
	'meaning': [],
	'phonetic': [],
	'origin': None
	}

	for span in spanList:
		meaningObj = {
			'category': None,
			'inflection': None,
			'definitions': []
		}

		defObj = {
			'serial' : None,
			'sense': None,
			'synonym': None,
			'notes': []		
						
		}
		pattern ='<span class="hw" data-headword-id="'
		if (pattern in span):
			wordObject['word'] = extractHeadWord(span)
		pattern ='<span class="pos">'
		if (pattern in span):
			category = extractContent(span)
			meaningObj['category'] = category
			wordObject['meaning'].append(meaningObj)
		pattern = '<span class="inflection-text">'
		if (pattern in span):
			inflection =  extractContent(span)
			wordObject['meaning'][-1]['inflection'] = inflection
		pattern = '<span class="iteration">'
		pattern2 = '<span class="subsenseIteration">'
		if (pattern in span or pattern2 in span):
			serial =  extractContent(span)
			defObj['serial'] = serial
			wordObject['meaning'][-1]['definitions'].append(defObj)
		pattern = '<span class="grammatical_note">'
		pattern2 = '<span class="sense-registers">'
		pattern3 = '<span class="sense-regions domain_labels">'
		if (pattern in span or pattern2 in span or pattern3 in span):
			note =  extractContent(span)
			if (len(wordObject['meaning'][-1]['definitions']) == 0 ):
				defObj['notes'].append(note)
				wordObject['meaning'][-1]['definitions'].append(defObj)
			else:
				wordObject['meaning'][-1]['definitions'][-1]['notes'].append(note)
		pattern = '<span class="ind">'
		if (pattern in span):
			sense =  extractContent(span)
			if (len(wordObject['meaning'][-1]['definitions']) == 0 ):
				defObj['sense'] = sense
				wordObject['meaning'][-1]['definitions'].append(defObj)
			else:
				wordObject['meaning'][-1]['definitions'][-1]['sense'] = sense
		pattern = '<span class="syn">'
		if (pattern in span):
			synonym =  extractContent(span)
			if (len(wordObject['meaning'][-1]['definitions']) == 0 ):
				defObj['synonym'] = synonym
				wordObject['meaning'][-1]['definitions'].append(defObj)
			else:
				wordObject['meaning'][-1]['definitions'][-1]['synonym'] = synonym
		pattern = '<span class="phoneticspelling">'	
		if (pattern in span):
			phonetic =  extractIPA(span)
			wordObject['phonetic'].append(phonetic)



	return (wordObject)


if __name__ == "__main__":
	wordObj = processPage(spans)
	print(wordObj)