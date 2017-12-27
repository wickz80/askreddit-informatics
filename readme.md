## askreddit-informatics

***

Askreddit-informatics pulls down questions and comments(answers) from the AskReddit subreddit on the site reddit.com.

It uses PRAW to talk to the reddit API, and SQLite3 to store data.  From each post, it gets:
* Post title (question)
* Upvotes (score)
* Created (UTC)
* reddit ID (link with comments)
* # comments
* URL

For each post, from the 'top' 10 comments:
* Post ID (reddit ID of post)
* Upvotes (score)
* Created (UTC)
* Body
* Parent comment ID (if it is a reply to an earlier comment)

The goal is to scrape Askreddit for a lot of text data, and then see what results from some analytics.  Down the line, this may become an ML experiment.
