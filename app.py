from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

dog_links = [
    {
        "title": "30 Fun and Fascinating Dog Facts",
        "url": "https://www.akc.org/expert-advice/lifestyle/dog-facts/",
        "score": 10,
    },
    {
        "title": "Why Do Dogs Tilt Their Heads?",
        "url": "https://www.sciencefocus.com/nature/why-do-dogs-tilt-their-head-when-you-speak-to-them",
        "score": 5,
    },
    {
        "title": "r/dogs — top posts",
        "url": "https://www.reddit.com/r/dogs/",
        "score": 3,
    },
    {
        "title": "Basic Dog Training Guide",
        "url": "https://www.animalhumanesociety.org/resource/how-get-most-out-training-your-dog",
        "score": 2,
    },
    {
        "title": "The Dogist (photo stories)",
        "url": "https://thedogist.com/",
        "score": 1,
    },
]


@app.get("/")
def homepage():
    return render_template("index.html", links=dog_links)

@app.post("/vote")
def vote():
    data = request.get_json()
    url = data.get("url")
    direction = data.get("direction")
    
    for post in dog_links:
        if post["url"] == url:
            if direction == "up":
                post["score"] += 1
            elif direction == "down":
                post["score"] -= 1
            return jsonify({"score": post["score"]})
    
    return jsonify({"error": "Link not found"}), 404