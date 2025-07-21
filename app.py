
from flask import Flask, render_template, request, redirect, url_for
from utils.slot_manager import get_available_slots, save_booking
import os
import sqlite3

app = Flask(__name__)

# Initialize DB if it doesn't exist
def init_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                postcode TEXT,
                service TEXT,
                date TEXT,
                time TEXT
            )
        """)
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        postcode = request.form["postcode"]
        service = request.form["service"]

        slots = get_available_slots(postcode, service)
        return render_template("calendar.html", name=name, phone=phone, postcode=postcode, service=service, slots=slots)

    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    data = {
        "name": request.form["name"],
        "phone": request.form["phone"],
        "postcode": request.form["postcode"],
        "service": request.form["service"],
        "date": request.form["date"],
        "time": request.form["time"]
    }
    save_booking(data)
    return render_template("success.html")

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
