import praw
import pprint
import sqlite3
import time
from itertools import islice
import credentials

reddit = praw.Reddit(client_id=credentials.login['clientID'],
                     client_secret=credentials.login['clientSecret'],
                     password=credentials.login['PASS'],
                     user_agent='ask reddit by /u/{}'.format(credentials.login['USER']),
                     username=credentials.login['USER'])

db = sqlite3.connect(r'C:\questions\questions.DB')
cur = db.cursor()

def populate_Existing_IDs():
	existing_ids = []
	try:
		cur.execute("SELECT reddit_id FROM posts")
		for id in cur.fetchall():
			existing_ids.append(id[0])
	except:
		pass
	return existing_ids

def get_MinTime():
	try:
		cur.execute("SELECT min(created_utc) FROM posts")
		minTime = float(cur.fetchone()[0])
	except:
		minTime = 'None'
	return minTime

print(get_MinTime())