import json, os, sys


def getFilePath(pathIn, dirOut):
	EXT = ".txt"
	temp_path = pathIn
	temp_path = os.path.basename(temp_path)
	fname, fext = os.path.splitext(temp_path)
	pathOut =  os.path.join(dirOut, fname + EXT) 
	#pathOut =  os.path.join(dirOut, FILNAME_OUT) 
	return pathOut



def openDir(targetdir):
	#open directory when done	
	rpath = os.path.realpath(targetdir)
	os.startfile(rpath)



def writeJSON(data, pathOut):
	with open(pathOut, 'w', encoding ="utf-8") as outfile:  
		json.dump(data, outfile)

def writeListToFile(vlist, vpath):
    with open(vpath, 'w', encoding ='utf-8') as file:
        for item in vlist:    
            file.write(item + "\n")