from bs4 import BeautifulSoup
from markdown import markdown
from gtts import gTTS
import creds
import praw

MIN_CHARACTERS = 1500
MAX_CHARACTERS = 3500

def markdown_to_text(markdown_string):
    html = markdown(markdown_string)
    soup = BeautifulSoup(html, 'html.parser')
    text = ''.join(soup.find_all(string=True))
    return text

def reddit_instance():
    reddit = praw.Reddit(
        client_id = creds.CLIENT_ID,
        client_secret = creds.CLIENT_SECRET,
        user_agent = creds.USER_AGENT
    )
    return reddit

def top_submission(reddit, subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    submissions = subreddit.top(limit=5, time_filter='day')
    for submission in submissions:
        if not (submission.link_flair_text in ("Modpost", "Breaking News") or submission.over_18):
            title_tts = gTTS(text=submission.title, lang="en")
            title_tts.save("media/tts/title.mp3")
            return submission

def top_comments(submission):
    comments_id = []
    char_counter = 0
    for comment in submission.comments:
        comment_body = markdown_to_text(comment.body)
        if comment_body in ("[deleted]", "[removed]"):
            continue
        char_counter += len(comment_body)
        if char_counter > MAX_CHARACTERS:
            return comments_id
        elif char_counter < MIN_CHARACTERS or len(comments_id) <= 6:
            comment_tts = gTTS(text=comment_body, lang="en")
            comment_tts.save(f"media/tts/{comment.id}.mp3")
            comments_id.append(comment.id)