## askreddit-informatics

***

Askreddit-informatics pulls down questions and comments(answers) from AskReddit on the site reddit.com.

It uses PRAW to talk to the reddit API, and SQLite3 to store data.  From each post, it gets:
* Post title (question)
* Upvotes (score)
* Created (UTC)
* Reddit ID (link with comments)
* Number of comments
* URL

For each post it grabs details about the 'top' 10 comments:
* Post ID (reddit ID of post)
* Upvotes (score)
* Created (UTC)
* Body
* Parent comment ID (if it is a reply to an earlier comment)

## Usage
***

To use askreddit-informatics, first populate credentials.py with your account information and Reddit app key/secret.

`cd \...yourDirectory..\askreddit-informatics\main`
`python grabData`
Stop the script -- then using Database4 or another SQL browser, run initdb.sql on the newly created questions.DB database.
`python grabData`
Once you've collected some data, use tokenizeDB to do some analysis.
`python tokenizeDB`

The goal is to scrape Askreddit for a lot of text data, and then see what results from some analytics.  Down the line, this may become an ML experiment.
