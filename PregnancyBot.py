import praw
import bot #custom, to store username and password info
import sqlite3 # database for storing comment IDs
import time

USERAGENT = """AmIPregnant_Bot - version 1.0 - https://github.com/escrimeuse/PregnancyBot"""
USERNAME = bot.un # reddit username
PASSWORD = bot.pw # reddit password
SUBREDDIT = "test"
MAXPOSTS = 10
SETPHRASES = [ "AM I PREGNANT", "COULD I BE PREGNANT", ]
SETRESPONSE = bot.message

WAIT = 300

# Create database for storing posts that have been replied to already
sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)")
sql.commit()
print("Opening database")

print("Logging in to reddit") # Log in to reddit
r=praw.Reddit(USERAGENT) #open a connection
r.login(USERNAME, PASSWORD) #log in



def replybot():
    print("Fetching subreddit", SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    
    print("Fetching submissions")
    submissions = subreddit.get_new(limit=MAXPOSTS) # call to reddit, gets MAXPOSTS items
    
    for submission in submissions: # goes through the submissions
        cur.execute("SELECT * FROM oldposts WHERE ID=?", [submission.id])
        if not cur.fetchone(): # if post has not been replied to already
            submissionTitle = submission.title.lower() # automatically convert title to lowercase
            if any(key.lower() in submissionTitle for key in SETPHRASES): 
                print("Replying to", submission.title)
                submission.add_comment(SETRESPONSE) # replies with comment              
            cur.execute("INSERT INTO oldposts VALUES(?)", [submission.id])
            sql.commit()

while True:
    replybot()
    time.sleep(WAIT)
