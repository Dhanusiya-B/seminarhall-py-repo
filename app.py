from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "pietech_secret"

# =========================
# ADMIN CREDENTIALS
# =========================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# =========================
# DATABASE CONNECTION
# =========================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          # XAMPP default password
        database="hall_booking"
    )

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/booking")
def booking():
    if "admin" not in session:
        return redirect(url_for("login"))
    return render_template("booking.html")


@app.route("/book", methods=["GET", "POST"])
def book():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        department = request.form['department']
        program_name = request.form["program_name"]
        booking_date = request.form["date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
    INSERT INTO bookings 
    (name, department, program_name, booking_date, start_time, end_time)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (name, department, program_name, booking_date, start_time, end_time))


        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("submit"))

    return render_template("booking.html")


@app.route("/submit")
def submit():
    if "admin" not in session:
        return redirect(url_for("login"))
    return render_template("submit.html")


@app.route("/view_bookings")
def view_bookings():
    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM bookings ORDER BY booking_date DESC")
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view_bookings.html", bookings=bookings)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =========================
# RUN APPLICATION
# =========================
if __name__ == "__main__":
    app.run(debug=True)
