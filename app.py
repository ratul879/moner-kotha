from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, secrets
from pathlib import Path
from functools import wraps

BASE = Path(__file__).resolve().parent
DB = BASE / "instance" / "moner_kotha.db"
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

ADMIN_ID = "admin"
ADMIN_PASSWORD = "MonerKotha@2026!"
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS appointments(
      id INTEGER PRIMARY KEY AUTOINCREMENT, booking_id TEXT UNIQUE,
      name TEXT, age TEXT, phone TEXT, email TEXT, service TEXT,
      media TEXT, date TEXT, time TEXT, message TEXT,
      status TEXT DEFAULT 'Pending', reply TEXT DEFAULT '',
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS messages(
      id INTEGER PRIMARY KEY AUTOINCREMENT, msg_id TEXT UNIQUE,
      kind TEXT, name TEXT, contact TEXT, title TEXT, message TEXT,
      status TEXT DEFAULT 'New', reply TEXT DEFAULT '',
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    con.commit(); con.close()

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper

@app.context_processor
def inject():
    return {"site_phone":"01735258091","site_name":"মনের কথা"}

@app.route("/")
def p1():
    return render_template("page1.html")

@app.route("/consultants")
def p2():
    return render_template("page2.html")

@app.route("/services")
def p3():
    return render_template("page3.html")

@app.route("/info")
def p4():
    return render_template("page4.html")

@app.route("/book", methods=["GET","POST"])
def book():
    if request.method == "POST":
        booking_id = "MK-" + secrets.token_hex(3).upper()
        data = request.form
        con=db()
        con.execute("""INSERT INTO appointments
          (booking_id,name,age,phone,email,service,media,date,time,message)
          VALUES(?,?,?,?,?,?,?,?,?,?)""",
          (booking_id,data.get("name"),data.get("age"),data.get("phone"),
           data.get("email"),data.get("service"),data.get("media"),
           data.get("date"),data.get("time"),data.get("message")))
        con.commit(); con.close()
        return render_template("success.html", ref=booking_id, typ="অ্যাপয়েন্টমেন্ট")
    return render_template("book.html")

@app.route("/anonymous", methods=["GET","POST"])
def anonymous():
    if request.method == "POST":
        msg_id = "MSG-" + secrets.token_hex(3).upper()
        d=request.form
        con=db(); con.execute("""INSERT INTO messages(msg_id,kind,name,contact,title,message)
            VALUES(?,?,?,?,?,?)""",
            (msg_id,"Anonymous Post","বেনামী",d.get("email",""),d.get("title"),d.get("message")))
        con.commit(); con.close()
        return render_template("success.html", ref=msg_id, typ="বেনামী বার্তা")
    return render_template("anonymous.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method=="POST":
        msg_id="CNT-"+secrets.token_hex(3).upper()
        d=request.form
        con=db(); con.execute("""INSERT INTO messages(msg_id,kind,name,contact,title,message)
            VALUES(?,?,?,?,?,?)""",
            (msg_id,"Contact",d.get("name"),d.get("contact"),d.get("title","যোগাযোগ"),d.get("message")))
        con.commit(); con.close()
        return render_template("success.html", ref=msg_id, typ="বার্তা")
    return render_template("contact.html")

@app.route("/status", methods=["GET","POST"])
def status():
    record=None
    if request.method=="POST":
        ref=request.form.get("ref","").strip()
        con=db()
        record=con.execute("SELECT * FROM appointments WHERE booking_id=?",(ref,)).fetchone()
        if not record:
            record=con.execute("SELECT * FROM messages WHERE msg_id=?",(ref,)).fetchone()
        con.close()
        if not record: flash("এই রেফারেন্স নম্বর পাওয়া যায়নি।")
    return render_template("status.html", record=record)

@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        uid=request.form.get("user_id","")
        pw=request.form.get("password","")
        if uid == ADMIN_ID and check_password_hash(ADMIN_PASSWORD_HASH, pw):
            session["admin"]=True; return redirect(url_for("dashboard"))
        flash("ID অথবা Password সঠিক নয়।")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear(); return redirect(url_for("admin_login"))

@app.route("/admin")
@admin_required
def dashboard():
    con=db()
    apps=con.execute("SELECT * FROM appointments ORDER BY id DESC").fetchall()
    msgs=con.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    con.close()
    return render_template("dashboard.html", appointments=apps, messages=msgs)

@app.route("/admin/appointment/<int:item_id>", methods=["POST"])
@admin_required
def update_appointment(item_id):
    d=request.form
    con=db(); con.execute("UPDATE appointments SET status=?, reply=? WHERE id=?",
        (d.get("status"),d.get("reply"),item_id)); con.commit(); con.close()
    return redirect(url_for("dashboard"))

@app.route("/admin/message/<int:item_id>", methods=["POST"])
@admin_required
def update_message(item_id):
    d=request.form
    con=db(); con.execute("UPDATE messages SET status=?, reply=? WHERE id=?",
        (d.get("status"),d.get("reply"),item_id)); con.commit(); con.close()
    return redirect(url_for("dashboard"))

if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0",port=5000,debug=False)
