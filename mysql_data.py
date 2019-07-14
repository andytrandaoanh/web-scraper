import mysql.connector
from mysql.connector import errorcode
from system_handler import writeListToFile, openDir

def get_connection(dbname=''):
	try:
		connection = mysql.connector.connect(
		user='andyanh', password='DGandyanh#1234',
	    host='127.0.0.1', database = dbname)
		if connection.is_connected():
			return connection 
	except Error as e:
		return e

def formatWordList(records):
	wordList = []
	for word in records:
		wordList.append(word[0])	
	return wordList

def getWordList():
	DB_NAME = "lexicon"
	db = get_connection(DB_NAME)
	cursor = db.cursor()
	select_sql= ("select distinct word from google_defs")
	try:
		cursor.execute(select_sql)
		records = cursor.fetchall()
		return formatWordList(records)
	except Exception as e:
		print("Error encountered:", e)
	finally:
		cursor.close
		db.close


if __name__ == "__main__":
	dirOut = "E:/FULLTEXT/SPECIALTY/"
	pathOut =  dirOut + "Dictionary_Headword_List.txt"
	wordList = getWordList()
	writeListToFile(wordList, pathOut)
	openDir(dirOut)