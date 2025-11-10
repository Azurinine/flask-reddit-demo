from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

dog_links = [
    {
        "id": 0,
        "title": "30 Fun and Fascinating Dog Facts",
        "url": "https://www.akc.org/expert-advice/lifestyle/dog-facts/",
        "score": 10,
        "hidden": False,
    },
    {
        "id": 1,
        "title": "Why Do Dogs Tilt Their Heads?",
        "url": "https://www.sciencefocus.com/nature/why-do-dogs-tilt-their-head-when-you-speak-to-them",
        "score": 5,
        "hidden": False,
    },
    {
        "id": 2,
        "title": "r/dogs — top posts",
        "url": "https://www.reddit.com/r/dogs/",
        "score": 3,
        "hidden": False,
    },
    {
        "id": 3,
        "title": "Basic Dog Training Guide",
        "url": "https://www.animalhumanesociety.org/resource/how-get-most-out-training-your-dog",
        "score": 2,
        "hidden": False,
    },
    {
        "id": 4,
        "title": "The Dogist (photo stories)",
        "url": "https://thedogist.com/",
        "score": 1,
        "hidden": False,
    },
]


@app.get("/")
def homepage():
    visible_links = [
        link for link in dog_links if not link.get("hidden", False)
    ]
    hidden_links = [link for link in dog_links if link.get("hidden", False)]

    visible_links = sorted(
        visible_links, key=lambda x: x["score"], reverse=True
    )
    hidden_links = sorted(hidden_links, key=lambda x: x["score"], reverse=True)

    error = request.args.get("error")
    return render_template(
        "index.html",
        links=visible_links,
        hidden_links=hidden_links,
        error=error,
    )


@app.post("/upvote/<int:link_id>")
def upvote(link_id):
    link = next((link for link in dog_links if link["id"] == link_id), None)
    if link:
        link["score"] += 1
    return redirect(url_for("homepage"))


@app.post("/downvote/<int:link_id>")
def downvote(link_id):
    link = next((link for link in dog_links if link["id"] == link_id), None)
    if link:
        link["score"] -= 1
    return redirect(url_for("homepage"))


@app.post("/hide/<int:link_id>")
def hide(link_id):
    for link in dog_links:
        if link["id"] == link_id:
            link["hidden"] = not link.get("hidden", False)
            break
    return redirect(url_for("homepage"))


@app.post("/submit")
def submit():
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()

    if not title:
        return redirect(url_for("homepage", error="Title cannot be empty"))

    if not url.startswith("http"):
        return redirect(url_for("homepage", error="URL must start with http"))

    # Create new post with next available ID
    new_id = max(link["id"] for link in dog_links) + 1 if dog_links else 0
    new_post = {
        "id": new_id,
        "title": title,
        "url": url,
        "score": 1,
        "hidden": False,
    }
    dog_links.append(new_post)

    return redirect(url_for("homepage"))
