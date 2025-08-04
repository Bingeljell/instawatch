# insta_watch.py
from itertools import islice
from instaloader import Instaloader, Profile

from db import init_db, get_connection, prune_posts

# 1) Hard-coded watch list; swap in your own handles
USERS = ["nike", "adidas"]
# 2) Number of recent posts to keep per user
N = 10

def main():
    init_db()

    loader = Instaloader(
        # download images from posts
        download_pictures=True,
        # download videos (including reels, IGTV clips, etc.)
        download_videos=True,
        # still skip comments (we don’t need their text)
        download_comments=False,
        # put all media under static/<username>/
        dirname_pattern="static/{target}"
    )

    for username in USERS:
        profile = Profile.from_username(loader.context, username)
        # fetch the first N posts
        for post in islice(profile.get_posts(), N):
            with get_connection() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO posts "
                    "(shortcode, username, date_utc, caption) "
                    "VALUES (?, ?, ?, ?)",
                    (
                        post.shortcode,
                        username,
                        post.date_utc.isoformat(),
                        post.caption or ""
                    )
                )
                conn.commit()
            loader.download_post(post, target=username)

        # prune old posts beyond the latest N
        prune_posts(username, N)
        print(f"[{username}] fetched ≤ {N} posts and pruned extras.")

if __name__ == "__main__":
    main()
