import re
from pprint import pprint
spans = [


'<p><a class="desktopCrumb home_breadcrumb_hide" data-behaviour="ga-event-breadcrumb" data-value="Homepage anchor" href="/en">Home</a> <span class="home_breadcrumb_hide"></span><a class="desktopCrumb" data-behaviour="ga-event-breadcrumb" data-value="Primary root" href="/en/english">British &amp; World English</a> <span></span> <a href="https://www.lexico.com/en/definition/accent">accent</a> </p>', 

'<span class="home_breadcrumb_hide"></span>', 

'<span class="hw" data-headword-id="accent">accent</span>',

'<span class="pos">noun</span>', 

'<span class="transitivity"></span>', 

'<span class="iteration">1</span>', 

'<span class="ind">A distinctive way of pronouncing a language, especially one associated with a particular country, area, or social class.</span>', 

'<strong class="syn">pronunciation</strong>', 

'<span class="syn">, intonation, enunciation, elocution, articulation, inflection, tone, modulation, cadence, timbre, utterance, manner of speaking, speech pattern, speech, diction, delivery</span>', 

'<span class="iteration">2</span>', 

'<span class="ind">A distinct emphasis given to a syllable or word in speech by stress or pitch.</span>', 

'<strong class="syn">stress</strong>', 

'<span class="syn">, emphasis, accentuation, force, prominence</span>', 

'<span class="subsenseIteration">2.1</span>', 

'<span class="ind">A mark on a letter, typically a vowel, to indicate pitch, stress, or vowel quality.</span>', 

'<strong class="syn">mark</strong>', 

'<span class="syn">, diacritic, diacritical mark, accent mark, sign</span>', 

'<span class="subsenseIteration">2.2</span>', 

'<span class="sense-regions domain_labels">Music </span>', 

'<span class="ind">An emphasis on a particular note or chord.</span>', 

'<span class="iteration">3</span>', 

'<span class="grammatical_note">in singular</span>', 

'<span class="ind">A special or particular emphasis.</span>', 

'<strong class="syn">emphasis</strong>', 

'<span class="syn">, stress, priority</span>', 

'<span class="subsenseIteration">3.1</span>', 

'<span class="ind">A feature which gives a distinctive visual emphasis to something.</span>', 

'<span class="pos">verb</span>', 

'<span class="iteration">1</span>', 

'<span class="ind">Emphasize (a particular feature)</span>', 

'<strong class="syn">focus attention on</strong>' 

'<span class="syn">, bring attention to, call attention to, draw attention to, point up, underline, underscore, accentuate, highlight, spotlight, foreground, feature, give prominence to, make more prominent, make more noticeable, play up, bring to the fore, heighten, stress, weight, emphasize, lay emphasis on, put emphasis on</span>', 

'<span class="subsenseIteration">1.1</span>', 

'<span class="sense-regions domain_labels">Music </span>', 

'<span class="ind">Play (a note or beat) with emphasis.</span>', 

'<strong>Origin</strong>', 

'<p>Late Middle English (in the sense ‘intonation’): from Latin accentus ‘tone, signal, or intensity’ (from ad- ‘to’ + cantus ‘song’), translating Greek prosōidia ‘a song sung to music, intonation’.</p>', 

'<span class="phoneticspelling">/ˈaks(ə)nt/</span>', 

'<span class="phoneticspelling">/ˈaksɛnt/</span>',

]

def extractP(myP):
	inputText = str(myP)
	outText = inputText.replace('<p>', '')
	outText = outText.replace('</p>', '')
	return str(outText)


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
		return(str(temp[1]))

def extractStrong(myStrong):
	inputText = str(myStrong)
	regPat = r'<strong class="[\w\-\s]+">[\w\s,().]+'
	pattern = re.compile(regPat)
	finds = re.findall(pattern, inputText)
	if(finds):
		find = finds[0]
		temp = find.split(">")
		return(str(temp[1]))

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
	'origin': None,
	'phonetic': []
	}



	flagOrigin = False
	stringSyn = ''
	flagPhrase = False

	for item in spanList:
		span = str(item)


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
			flagPhrase = False
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

		pattern = '<strong class="phrase">'
		if (pattern in span):
			flagPhrase = True

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
		if (pattern in span and not flagPhrase):
			sense =  extractContent(span)
			if (len(wordObject['meaning'][-1]['definitions']) == 0 ):
				defObj['sense'] = sense
				wordObject['meaning'][-1]['definitions'].append(defObj)
			else:
				wordObject['meaning'][-1]['definitions'][-1]['sense'] = sense

		pattern = '<strong class="syn">'
		if (pattern in span):
			stringSyn =  extractStrong(span)

		pattern = '<span class="syn">'
		if (pattern in span):
			synonym =  stringSyn + extractContent(span)
			stringSyn = ''

			if (len(wordObject['meaning'][-1]['definitions']) == 0 ):
				defObj['synonym'] = synonym
				wordObject['meaning'][-1]['definitions'].append(defObj)
			else:
				wordObject['meaning'][-1]['definitions'][-1]['synonym'] = synonym
		pattern = '<span class="phoneticspelling">'	
		if (pattern in span):
			phonetic =  extractIPA(span)
			wordObject['phonetic'].append(phonetic)
		pattern = '<strong>Origin</strong>'	
		if (pattern in span):
			flagOrigin = True
		pattern = '<p>'	
		if (pattern in span and flagOrigin):
			wordObject['origin'] = extractP(span)
			flagOrigin = False


	return (wordObject)


if __name__ == "__main__":
	wordObj = processPage(spans)
	pprint(wordObj)