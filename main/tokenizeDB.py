import praw
import sqlite3
import time
from itertools import islice
import re
import csv
from multiprocessing import Pool as ThreadPool

def fetchAllPostText(amount):
	if amount == 0:
		cur.execute("SELECT title FROM posts WHERE score >= 1")
	else:
		cur.execute("SELECT title FROM posts WHERE score >= 1 LIMIT {}".format(amount))
	return cur.fetchall()

def tokenizeDbIntoSet(dbTextList):
	wordList = []
	for dbText in dbTextList:
		formattedText = re.sub('[^a-zA-Z -/]+', '', str(dbText[0]).lower())
		textWords = re.split("[ -/]+", formattedText, flags=re.IGNORECASE)
		for textWord in textWords:
			try:
				wordList += [textWord]
			except Exception as e:
				print("Error...",e)
	return set(wordList)

def getAverageScore(key, cur):
	query = """SELECT round(avg(score),1) 
				FROM posts 
				WHERE title 
				LIKE {wildcard}
				AND 
					(SELECT count(*) 
					 FROM posts
					 WHERE title 
					 LIKE {wildcard}) > 1
				""".format(wildcard='\'%{term}%\'').format(term=key)
	cur.execute(query)
	return cur.fetchone()[0]

def getOccurences(key, cur):
	query = """SELECT count(*)
				FROM posts
				WHERE title 
				LIKE {wildcard}
				""".format(wildcard='\'%{term}%\'').format(term=key)
	cur.execute(query)
	return cur.fetchone()[0]

def buildTuple(wordSet, cur):
	setLength = len(wordSet)
	wordTuple = [('word', 'avgScore', 'numOccurences')]
	startTime = time.time()
	for i, textWord in enumerate(wordSet):
		wordTuple += [(textWord, getAverageScore(textWord, cur), getOccurences(textWord, cur))]
		if i % 50 == 0:
			estimateProgess(i, setLength, startTime)
	return wordTuple
		
def estimateProgess(currentIteration, totalIterations, lastTimestamp):
	try:
		fractionDone = currentIteration/totalIterations
		percentageDone = round((fractionDone*100),2)
		elapsedTime = round(time.time()-lastTimestamp,2)
		secondsUntilDone = ((1/fractionDone) * elapsedTime)-elapsedTime
		completionEstimate = time.strftime("%H:%M:%S", time.gmtime(secondsUntilDone))
		
	except:
		fractionDone = currentIteration/totalIterations
		percentageDone = round((fractionDone*100),2)
		elapsedTime = round(time.time()-lastTimestamp,2)
		secondsUntilDone = 1
		completionEstimate = time.strftime("%H:%M:%S", time.gmtime(secondsUntilDone))

	statusText = '{} out of {} iterations performed -- {}%\n'.format(str(currentIteration),str(totalIterations),str(percentageDone))
	timeChange = ' Time elapsed: {} seconds\n'.format(time.strftime("%H:%M:%S", time.gmtime(elapsedTime)))
	timeEstimate = ' Estimated time until completion: {}\n'.format(completionEstimate)
	print(statusText, timeChange, timeEstimate)

def writeTupleToCSV(tuple, fileName):
	with open('{}.csv'.format(fileName), 'w', newline='') as csv_file:
	    writer = csv.writer(csv_file)
	    for line in tuple:
	    	try:
	    		writer.writerow(line)
	    	except Exception as e:
	    		print("Error...",e)

db = sqlite3.connect(r'questions.DB')
cur = db.cursor()
#pool = ThreadPool(4)
askRedditPosts = fetchAllPostText(1000)
wordSet = tokenizeDbIntoSet(askRedditPosts)
wordTuple = buildTuple(wordSet, cur)

for line in wordTuple:
	print(line)

writeTupleToCSV(wordTuple, 'tupleList')



