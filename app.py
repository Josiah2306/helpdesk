from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)


# --------------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and user["password"] == password:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")



# --------------------------------------------------------
# LOGOUT
# --------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# --------------------------------------------------------
# DASHBOARD
# --------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM tickets")
    total_tickets = cursor.fetchone()["total"]

    return render_template("dashboard.html", total=total_tickets)


# --------------------------------------------------------
# LIST TICKETS
# --------------------------------------------------------
@app.route("/tickets")
def tickets():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session["role"]
    user_id = session["user_id"]

    cursor = mysql.connection.cursor()

    if role == "ADMIN" or role == "AGENT":
        cursor.execute("""
            SELECT tickets.*, users.username 
            FROM tickets
            JOIN users ON tickets.user_id = users.id
        """)
    else:
        cursor.execute("""
            SELECT tickets.*, users.username 
            FROM tickets
            JOIN users ON tickets.user_id = users.id
            WHERE user_id = %s
        """, (user_id,))

    data = cursor.fetchall()

    return render_template("tickets_list.html", tickets=data)


# --------------------------------------------------------
# NEW TICKET
# --------------------------------------------------------
@app.route("/tickets/new", methods=["GET", "POST"])
def ticket_new():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        user_id = session["user_id"]

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO tickets (title, description, user_id)
            VALUES (%s, %s, %s)
        """, (title, description, user_id))

        mysql.connection.commit()
        return redirect("/tickets")

    return render_template("ticket_new.html")


# --------------------------------------------------------
# TICKET DETAILS + COMMENTS
# --------------------------------------------------------
@app.route("/tickets/<int:ticket_id>", methods=["GET", "POST"])
def ticket_detail(ticket_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    # Get ticket
    cursor.execute("""
        SELECT tickets.*, users.username
        FROM tickets
        JOIN users ON tickets.user_id = users.id
        WHERE tickets.id = %s
    """, (ticket_id,))
    ticket = cursor.fetchone()

    # Get comments
    cursor.execute("""
        SELECT ticket_comments.*, users.username
        FROM ticket_comments
        JOIN users ON ticket_comments.user_id = users.id
        WHERE ticket_comments.ticket_id = %s
        ORDER BY created_at ASC
    """, (ticket_id,))
    comments = cursor.fetchall()

    # Add comment
    if request.method == "POST":
        comment = request.form["comment"]
        user_id = session["user_id"]

        cursor.execute("""
            INSERT INTO ticket_comments (ticket_id, user_id, comment)
            VALUES (%s, %s, %s)
        """, (ticket_id, user_id, comment))
        mysql.connection.commit()

        return redirect(f"/tickets/{ticket_id}")

    return render_template("ticket_detail.html", ticket=ticket, comments=comments)

@app.route("/tickets/<int:ticket_id>/delete", methods=["POST"])
def delete_ticket(ticket_id):
    # Only ADMIN or AGENT can delete tickets
    if session.get("role") not in ("ADMIN", "AGENT"):
        flash("You do not have permission to delete tickets.")
        return redirect("/tickets")

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM ticket_comments WHERE ticket_id=%s", (ticket_id,))
    cursor.execute("DELETE FROM tickets WHERE id=%s", (ticket_id,))
    mysql.connection.commit()

    flash("Ticket deleted successfully.")
    return redirect("/tickets")

@app.route("/users")
def users_list():
    if "user_id" not in session or session.get("role") != "ADMIN":
        flash("Access denied.")
        return redirect("/dashboard")

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users")
    users = cursor.fetchall()

    return render_template("users_list.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)

