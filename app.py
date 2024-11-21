import praw
import streamlit as st
import requests

# Function to check if URL is an image or valid image link
def is_valid_image(url):
    try:
        if "i.redd.it" in url or "imgur.com" in url:
            return True
        response = requests.head(url)
        content_type = response.headers.get("content-type")
        return content_type.startswith("image")
    except:
        return False

# Set up Reddit API
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="StreamlitRedditApp",
    check_for_async=False
)

# Streamlit app
st.title("Reddit Image Gallery (Including NSFW)")

subreddit_name = st.text_input("Enter subreddit name:")
if subreddit_name:
    try:
        # Fetch the subreddit
        subreddit = reddit.subreddit(subreddit_name)
        st.write(f"Showing posts from: r/{subreddit_name}")

        # Create columns for gallery
        columns = st.columns(3)  # Adjust the number for more/less columns (e.g., 3 for 3 images per row)

        # Fetch top 10 hot posts and display images
        column_index = 0
        for post in subreddit.hot(limit=10):  # Adjust limit as needed
            if is_valid_image(post.url):  # Check if the URL is a valid image
                with columns[column_index]:
                    st.image(post.url, caption=post.title, use_column_width=True)
                column_index += 1
                if column_index >= len(columns):
                    column_index = 0  # Reset column index to 0 to start a new row

    except Exception as e:
        st.error(f"Error fetching subreddit: {e}")
