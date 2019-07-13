import json, os, sys


def openDir(targetdir):
	#open directory when done	
	rpath = os.path.realpath(targetdir)
	os.startfile(rpath)



def writeJSON(data, pathOut):
	with open(pathOut, 'w', encoding ="utf-8") as outfile:  
		json.dump(data, outfile)