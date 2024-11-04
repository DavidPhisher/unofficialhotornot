from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import random

app = Flask(__name__)

# Connect to the database and create a table for images and votes
def init_db():
    with sqlite3.connect("facemash.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT UNIQUE NOT NULL,
                score INTEGER DEFAULT 0
            )"""
        )
        conn.commit()

# Add images to the database if not already added
def add_images():
    image_folder = "static/images/"
    with sqlite3.connect("facemash.db") as conn:
        cursor = conn.cursor()
        for image in os.listdir(image_folder):
            cursor.execute("INSERT OR IGNORE INTO images (image_path) VALUES (?)", (f"{image_folder}{image}",))
        conn.commit()

# Fetch two random images for voting, along with their scores
def get_two_images():
    with sqlite3.connect("facemash.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images ORDER BY RANDOM() LIMIT 2")
        return cursor.fetchall()

@app.route("/")
def index():
    images = get_two_images()
    return render_template("index.html", images=images)

@app.route("/vote", methods=["POST"])
def vote():
    data = request.json
    winner_id = data["winner_id"]

    with sqlite3.connect("facemash.db") as conn:
        cursor = conn.cursor()
        # Increment the score of the selected image
        cursor.execute("UPDATE images SET score = score + 1 WHERE id = ?", (winner_id,))
        conn.commit()

    # Fetch the updated scores for both images
    images = get_two_images()
    return jsonify(images=images)

if __name__ == "__main__":
    init_db()
    add_images()
    app.run(debug=True)
