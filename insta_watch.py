from instaloader import Instaloader, Profile

loader = Instaloader(download_pictures=False,
                     download_videos=False,
                     download_comments=False)

profile = Profile.from_username(loader.context, "instagram")
for post in profile.get_posts():
    print(post.shortcode, post.date_utc)
    break
