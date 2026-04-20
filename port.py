from flask import Flask, redirect, render_template, request
import sqlite3
import os
from datetime import datetime

app=Flask(__name__)

rv_path= os.path.join(os.path.dirname(__file__), 'review.db')

def get_db_connection():
    conn= sqlite3.connect(rv_path)
    return conn

def init_db():
    conn=get_db_connection()
    c  =conn.cursor()
    c.execute("""
        CREATE A TABLE IF NOT EXISTS reviews(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              review TEXT NIT NULL,
              rating INTEGER NOT NULL,
              date TEXT DEFAULT CURRENT_TIMESTAMP

            )
    """
)
    conn.commit()
    conn.close()


@app.route("/")
def home():

    conn = get_db_connection()
    reviews = conn.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("index.html", reviews=reviews)
    

@app.route("/review", methods=["GET", "POST"])
def review():

    if request.method == "POST":
        name = request.form["name"]
        review = request.form["review"]
        rating = request.form["rating"]

        conn = get_db_connection()
        c = conn.cursor()

        c.execute(
            "INSERT INTO reviews (name, review, rating) VALUES (?, ?, ?)",
            (name, review, rating)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("review.html")

