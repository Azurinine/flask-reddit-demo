import sqlite3

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE = "reddit.db"


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with schema and default data."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            score INTEGER DEFAULT 1,
            hidden INTEGER DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM posts")
    count = cursor.fetchone()[0]

    if count == 0:
        default_posts = [
            (
                "30 Fun and Fascinating Dog Facts",
                "https://www.akc.org/expert-advice/lifestyle/dog-facts/",
                10,
                0,
            ),
            (
                "Why Do Dogs Tilt Their Heads?",
                "https://www.sciencefocus.com/nature/why-do-dogs-tilt-their-head-when-you-speak-to-them",
                5,
                0,
            ),
            ("r/dogs — top posts", "https://www.reddit.com/r/dogs/", 3, 0),
            (
                "Basic Dog Training Guide",
                "https://www.animalhumanesociety.org/resource/how-get-most-out-training-your-dog",
                2,
                0,
            ),
            ("The Dogist (photo stories)", "https://thedogist.com/", 1, 0),
        ]
        cursor.executemany(
            "INSERT INTO posts (title, url, score, hidden) VALUES (?, ?, ?, ?)",
            default_posts,
        )

    conn.commit()
    conn.close()


# Initialize database on startup
init_db()


@app.get("/")
def homepage():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE hidden = 0 ORDER BY score DESC")
    visible_links = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM posts WHERE hidden = 1 ORDER BY score DESC")
    hidden_links = [dict(row) for row in cursor.fetchall()]

    conn.close()

    error = request.args.get("error")
    return render_template(
        "index.html",
        links=visible_links,
        hidden_links=hidden_links,
        error=error,
    )


@app.post("/upvote/<int:link_id>")
def upvote(link_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE posts SET score = score + 1 WHERE id = ?", (link_id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("homepage"))


@app.post("/downvote/<int:link_id>")
def downvote(link_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE posts SET score = score - 1 WHERE id = ?", (link_id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("homepage"))


@app.post("/hide/<int:link_id>")
def hide(link_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT hidden FROM posts WHERE id = ?", (link_id,))
    row = cursor.fetchone()

    if row:
        new_hidden = 1 - row["hidden"]
        cursor.execute(
            "UPDATE posts SET hidden = ? WHERE id = ?", (new_hidden, link_id)
        )
        conn.commit()

    conn.close()
    return redirect(url_for("homepage"))


@app.post("/submit")
def submit():
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()

    if not title:
        return redirect(url_for("homepage", error="Title cannot be empty"))

    if not url.startswith("http"):
        return redirect(url_for("homepage", error="URL must start with http"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (title, url, score, hidden) VALUES (?, ?, 1, 0)",
        (title, url),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("homepage"))
