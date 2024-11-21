import praw
import streamlit as st
import requests

# Function to check if URL is an image
def is_image(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get("content-type")
        return content_type.startswith("image")
    except:
        return False

# Set up Reddit API with NSFW allowed
reddit = praw.Reddit(
    client_id="lCQo5bQ4ITrCIDFnwvApAA",
    client_secret="0tZuN3EdSsGfJmq58KI5BuL8qtFqTQ",
    user_agent="StreamlitRedditApp",
    check_for_async=False
)
reddit.config._allowNSFW = True
# Streamlit app
st.title("Reddit Image Viewer (Including NSFW)")

subreddit_name = st.text_input("Enter subreddit name:")
if subreddit_name:
    try:
        # Fetch the subreddit
        subreddit = reddit.subreddit(subreddit_name)
        st.write(f"Showing posts from: r/{subreddit_name}")

        # Fetch top 10 hot posts and display images
        for post in subreddit.hot(limit=10):
            st.write(f"Post URL: {post.url}")
            st.write(f"Is NSFW: {post.over_18}")
            if is_image(post.url):
                st.image(post.url, caption=post.title)
            else:
                st.write(f"Not an image or unsupported URL: {post.url}")

                
    except Exception as e:
        st.error(f"Error fetching subreddit: {e}")
