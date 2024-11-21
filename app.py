import praw
import streamlit as st

# Connect to Reddit API
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="StreamlitRedditApp",
    check_for_async=False
)
#reddit.read_only = False
reddit.config._allowNSFW = True

# App title
st.title("Reddit Image Fetcher")

# User input for subreddit
subreddit_name = st.text_input("Enter a subreddit name (e.g., 'aww', 'pics', 'earthporn'):", "")

if subreddit_name:
    # Fetch subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Display top images
    st.header(f"Top images from r/{subreddit_name}")
    posts = []
    for post in subreddit.hot(limit=10):  # Adjust limit as needed
        if post.url.endswith((".jpg", ".png", ".jpeg")):
            posts.append({"title": post.title, "url": post.url})
    
    if posts:
        for post in posts:
            st.subheader(post["title"])
            st.image(post["url"])
    else:
        st.warning(f"No images found in r/{subreddit_name}")
