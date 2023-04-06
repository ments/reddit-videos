from scrape_reddit import reddit_instance, top_submission, top_comments
from screenshots import take_screenshots
from video import make_video

SUBREDDIT = "AskReddit"

def main():
    
    reddit = reddit_instance()
    submission = top_submission(reddit, SUBREDDIT)
    comments_id = top_comments(submission)

    take_screenshots(SUBREDDIT, submission.id, comments_id)



if __name__ == "__main__":
    main()