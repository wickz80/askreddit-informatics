import praw
import pprint
import sqlite3
import time
from itertools import islice
from . import credentials

reddit = praw.Reddit(client_id=clientID,
                     client_secret=clientSecret,
                     password=PASS,
                     user_agent='ask reddit by /u/{}'.format(USER),
                     username=USER)

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

def insert_Post(db, submission):
	db.execute\
		("INSERT INTO posts (reddit_id, created_utc, title, content, num_comments, score, url) VALUES (?,?,?,'empty',?,?,?)",
		(submission.id, submission.created_utc, submission.title, submission.num_comments, submission.score, submission.url))

def insert_TopX_Comments(db, submission, limit):
	submission.comment_sort = 'top'
	comments = submission.comments.list()
	for comment in islice(comments, 0, limit):
		db.execute\
			("INSERT INTO comments (post_id, created_utc, body, score, parent_comment) VALUES (?,?,?,?,'')",
			(submission.id, comment.created_utc, comment.body, comment.score))


postList = reddit.subreddit('askreddit')
existing_ids = populate_Existing_IDs()
postCount = 0

for submission in postList.submissions(start=None, end=get_MinTime()):
	
	postCount += 1
	print(postCount,":",submission.title)
	
	try:	
		if submission.id not in existing_ids:
			insert_Post(db, submission)
			insert_TopX_Comments(db, submission, 10)

	except Exception as e:
		print("Error... :", e)

	if postCount % 100 == 0:
		db.commit()

	if postCount == 150000:
		break


	

db.commit()
db.close()
	
