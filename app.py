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
    return render_template("index.html", links=sorted(dog_links, key=lambda x : -x["score"]))

@app.post("/create")
def create():
    data = request.get_json()
    title = data.get("title", "").strip()
    url = data.get("url", "").strip()
    
    if not title or len(title) == 0:
        return jsonify({"error": "Title is required"}), 400
    
    if len(title) > 200:  # Reasonable limit
        return jsonify({"error": "Title is too long (max 200 characters)"}), 400
    
    if not url or len(url) == 0:
        return jsonify({"error": "URL is required"}), 400
    
    # Validate URL starts with http:// or https://
    if not url.startswith("http://") and not url.startswith("https://"):
        return jsonify({"error": "URL must start with http:// or https://"}), 400
    
    # Check if URL already exists
    for link in dog_links:
        if link["url"] == url:
            return jsonify({"error": "This URL already exists"}), 400
    
    # If all validation passes, create the new link
    new_link = {
        "title": title,
        "url": url,
        "score": 1
    }
    dog_links.append(new_link)
    
    return jsonify({"success": True}), 201

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