CREATE TABLE posts
(reddit_id TEXT, created_utc REAL, title TEXT,
content TEXT, num_comments INTEGER, score INTEGER, url TEXT)

CREATE TABLE comments
(post_id TEXT, created_utc REAL, body TEXT, 
score INTEGER, parent_comment INTEGER)