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
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
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
        for post in subreddit.hot(limit=10):  # Adjust limit as needed
            if is_image(post.url):  # Check if the URL points to an image
                st.image(post.url, caption=post.title)
                
    except Exception as e:
        st.error(f"Error fetching subreddit: {e}")
