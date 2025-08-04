import sqlite3
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
import glob, os, mimetypes

DB_PATH = "instawatch.db"
FEED_FILE = "instawatch.xml"
BASE_INSTAGRAM_URL = "https://www.instagram.com/p/"
MEDIA_BASE_URL = "http://localhost:8000/static"
MEDIA_DIR = "static"

def get_posts(limit=100):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT username, shortcode, date_utc, caption
          FROM posts
      ORDER BY date_utc DESC
         LIMIT ?
    """, (limit,))
    return cur.fetchall()

def generate_feed():
    fg = FeedGenerator()
    fg.title("InstaWatch Aggregated Feed")
    fg.link(href="https://example.com/instawatch.xml", rel="self")
    fg.description("Latest posts from your watched Instagram profiles")
    fg.language("en")

    for row in get_posts():
        fe = fg.add_entry()
        post_url = f"{BASE_INSTAGRAM_URL}{row['shortcode']}/"
        fe.id(post_url)
        fe.link(href=post_url)
        fe.title(f"{row['username']}: {row['caption'][:30] or 'No caption'}")

        # timezone-aware pubDate
        dt = datetime.fromisoformat(row["date_utc"]).replace(tzinfo=timezone.utc)
        fe.pubDate(dt)

        # build timestamp pattern to match Instaloader filenames
        ts = datetime.fromisoformat(row["date_utc"]) \
               .strftime("%Y-%m-%d_%H-%M-%S_UTC")
        pattern = os.path.join(MEDIA_DIR, row["username"], f"{ts}*.*")

        # find all media files for this post
        media_files = []
        for filepath in glob.glob(pattern):
            mtype, _ = mimetypes.guess_type(filepath)
            # only images and videos
            if not mtype or not (mtype.startswith("image/") or mtype.startswith("video/")):
                continue
            media_files.append({
                "path": filepath,
                "url": filepath.replace(MEDIA_DIR, MEDIA_BASE_URL),
                "type": mtype,
                "size": os.path.getsize(filepath)
            })

        # --- BACKWARDS-COMPATIBLE single enclosure (optional) ---
        if media_files:
            mf = media_files[0]
            fe.enclosure(url=mf["url"], length=str(mf["size"]), type=mf["type"])

        # build a rich HTML block for content:encoded
        html_parts = []
        if row["caption"]:
            # simple paragraph for caption
            html_parts.append(f"<p>{row['caption']}</p>")
        for mf in media_files:
            if mf["type"].startswith("image/"):
                html_parts.append(f'<img src="{mf["url"]}" alt="" />')
            else:  # video
                html_parts.append(
                    f'<video controls width="100%">'
                    f'<source src="{mf["url"]}" type="{mf["type"]}">'
                    f'Your browser does not support the video tag.'
                    f'</video>'
                )

        # wrap in CDATA so it’s preserved as HTML
        fe.content("<![CDATA[\n" + "\n".join(html_parts) + "\n]]>", type="CDATA")

    # write RSS 2.0
    fg.rss_file(FEED_FILE)
    print(f"Generated feed: {FEED_FILE}")

if __name__ == "__main__":
    generate_feed()
