from screenshots import take_screenshots
from gtts import gTTS
import creds
import praw
import re

SUBREDDIT = "AskReddit"
MIN_CHARACTERS = 2000
MAX_CHARACTERS = 3500

def top_submission(reddit, subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    submissions = subreddit.top(limit=5, time_filter='day')
    for submission in submissions:
        if not (submission.link_flair_text in ("Modpost", "Breaking News") or submission.over_18):
            return submission

def top_comments(submission):
    comments = submission.comments
    comments_id = []
    c_counter = 0
    for index, comment in enumerate(comments):
        c_counter += len(comment.body)
        if c_counter > MAX_CHARACTERS:
            return comments_id
        elif c_counter < MIN_CHARACTERS or index <= 6:
            comment_tts = gTTS(text=comment.body, lang="en")
            comment_tts.save(f"comment{index}.mp3")
            comments_id.append(comment.id)

def main():
    reddit = praw.Reddit(
        client_id = creds.CLIENT_ID,
        client_secret = creds.CLIENT_SECRET,
        user_agent = creds.USER_AGENT
    )
    submission = top_submission(reddit, SUBREDDIT)

    title_tts = gTTS(text=submission.title, lang="en")
    title_tts.save("title.mp3")

    comments_id = top_comments(submission)
    take_screenshots(submission.id, comments_id)
    


if __name__ == "__main__":
    main()