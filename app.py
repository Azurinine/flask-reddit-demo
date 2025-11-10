from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

dog_links = [
    {
        "id": 0,
        "title": "30 Fun and Fascinating Dog Facts",
        "url": "https://www.akc.org/expert-advice/lifestyle/dog-facts/",
        "score": 10,
    },
    {
        "id": 1,
        "title": "Why Do Dogs Tilt Their Heads?",
        "url": "https://www.sciencefocus.com/nature/why-do-dogs-tilt-their-head-when-you-speak-to-them",
        "score": 5,
    },
    {
        "id": 2,
        "title": "r/dogs — top posts",
        "url": "https://www.reddit.com/r/dogs/",
        "score": 3,
    },
    {
        "id": 3,
        "title": "Basic Dog Training Guide",
        "url": "https://www.animalhumanesociety.org/resource/how-get-most-out-training-your-dog",
        "score": 2,
    },
    {
        "id": 4,
        "title": "The Dogist (photo stories)",
        "url": "https://thedogist.com/",
        "score": 1,
    },
]


@app.get("/")
def homepage():
    links = sorted(dog_links, key=lambda x: x["score"], reverse=True)
    return render_template("index.html", links=links)


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
