sqlite3 instawatch.db <<'EOF'
CREATE TABLE IF NOT EXISTS posts (
  shortcode   TEXT    PRIMARY KEY,
  date_utc    TEXT    NOT NULL,
  caption     TEXT,
  fetched_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
EOF
