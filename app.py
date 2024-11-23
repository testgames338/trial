import praw
import streamlit as st
import random

# Set up Reddit API
reddit = praw.Reddit(
    client_id="lCQo5bQ4ITrCIDFnwvApAA",
    client_secret="0tZuN3EdSsGfJmq58KI5BuL8qtFqTQ",
    user_agent="StreamlitRedditApp",
    check_for_async=False
)

# Function to check if a post has a gallery and extract image URLs
def get_gallery_images(post):
    image_urls = []
    if hasattr(post, "media_metadata"):  # Check if the post has media_metadata (gallery)
        for item in post.media_metadata.values():
            # Extract the "s" (source) URL, which is the highest quality
            image_url = item.get("s", {}).get("u")
            if image_url:
                image_urls.append(image_url.replace("&amp;", "&"))  # Fix URL encoding issues
    return image_urls

# Streamlit app
st.title("Reddit Post Gallery Viewer")

subreddit_name = st.text_input("Enter subreddit name:")
if subreddit_name:
    try:
        # Fetch the subreddit
        subreddit = reddit.subreddit(subreddit_name)
        st.write(f"Showing posts from: r/{subreddit_name}")

        # Fetch the top 10 hot posts
        for post in subreddit.hot(limit=100):  # Adjust limit as needed
            #st.subheader(post.title)

            # Extract and display images from the gallery
            gallery_images = get_gallery_images(post)
            if gallery_images:
                #st.write("Gallery Images:")
                # Randomize the images for display
                random.shuffle(gallery_images)
                for image_url in gallery_images:
                    st.image(image_url, caption=post.title, width=700)
            else:
                # Handle non-gallery posts with single images
                if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    st.image(post.url, caption=post.title, width=700)
                else:
                    pass
                    #st.write("This post does not contain displayable images.")
    except Exception as e:
        st.error(f"Error fetching subreddit: {e}")
