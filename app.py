from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import pickle
from werkzeug.security import generate_password_hash, check_password_hash
from report_utils import create_pdf
from flask import send_file

app = Flask(__name__)
app.secret_key = "supersecretkey"

model = pickle.load(open("models/model.pkl","rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl","rb"))

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, username TEXT, news TEXT, prediction TEXT, confidence REAL)")
    conn.commit()
    conn.close()
init_db()

def is_logged_in(): return "user" in session
def is_admin(): return session.get("user")=="Mounidharan"

def explain_prediction(text, vec):
    feature_names = vectorizer.get_feature_names_out()
    dense = vec.toarray()[0]
    idx = dense.argsort()[-8:][::-1]
    return [feature_names[i] for i in idx if dense[i]>0]

def highlight_text(text, keywords):
    words = text.split()
    return " ".join([f"<span class='highlight'>{w}</span>" if w.lower().strip(".,!?") in keywords else w for w in words])

@app.route("/")
def home():
    if not is_logged_in(): return redirect("/login")
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        user=request.form["username"]
        pwd=generate_password_hash(request.form["password"])
        conn=sqlite3.connect("users.db")
        try:
            conn.execute("INSERT INTO users VALUES(NULL,?,?)",(user,pwd))
            conn.commit()
        except:
            return "User exists ❌"
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        user=request.form["username"]
        pwd=request.form["password"]
        conn=sqlite3.connect("users.db")
        cur=conn.cursor()
        cur.execute("SELECT password FROM users WHERE username=?",(user,))
        data=cur.fetchone()
        conn.close()
        if data and check_password_hash(data[0],pwd):
            session["user"]=user
            return redirect("/")
        return "Invalid ❌"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")

@app.route("/predict", methods=["POST"])
def predict():
    if not is_logged_in():
        return redirect("/login")

    text = request.form["news"]
    vec = vectorizer.transform([text])

    pred = model.predict(vec)[0]
    probs = model.predict_proba(vec)[0]

    fake_score = round(probs[0] * 100, 2)
    real_score = round(probs[1] * 100, 2)

    result = "REAL" if pred == 1 else "FAKE"
    confidence = max(fake_score, real_score)

    keywords = explain_prediction(text, vec)
    highlighted = highlight_text(text, keywords)

    # store history
    conn = sqlite3.connect("users.db")
    conn.execute(
        "INSERT INTO history VALUES(NULL,?,?,?,?)",
        (session["user"], text, result, confidence)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "prediction": result,
        "confidence": confidence,
        "fake_score": fake_score,
        "real_score": real_score,
        "keywords": keywords,
        "highlighted": highlighted
    })
@app.route("/history")
def history():
    if not is_logged_in(): return redirect("/login")
    conn=sqlite3.connect("users.db")
    data=conn.execute("SELECT news,prediction,confidence FROM history WHERE username=?",(session["user"],)).fetchall()
    conn.close()
    return render_template("history.html",data=data)

@app.route("/dashboard")
def dashboard():
    if not is_logged_in(): return redirect("/login")
    conn=sqlite3.connect("users.db")
    cur=conn.cursor()
    cur.execute("SELECT COUNT(*) FROM history WHERE username=?",(session["user"],))
    total=cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM history WHERE username=? AND prediction='REAL'",(session["user"],))
    real=cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM history WHERE username=? AND prediction='FAKE'",(session["user"],))
    fake=cur.fetchone()[0]
    cur.execute("SELECT news,prediction,confidence FROM history WHERE username=? ORDER BY id DESC LIMIT 5",(session["user"],))
    recent=cur.fetchall()
    conn.close()
    return render_template("dashboard.html",total=total,real=real,fake=fake,recent=recent)

@app.route("/admin")
def admin():
    if not is_admin(): return "Access Denied ❌"
    conn=sqlite3.connect("users.db")
    users=conn.execute("SELECT username FROM users").fetchall()
    history=conn.execute("SELECT username,news,prediction,confidence FROM history").fetchall()
    conn.close()
    return render_template("admin.html",users=users,history=history)

@app.route("/delete_user/<username>")
def delete_user(username):
    if not is_admin(): return "Denied ❌"
    conn=sqlite3.connect("users.db")
    conn.execute("DELETE FROM users WHERE username=?",(username,))
    conn.execute("DELETE FROM history WHERE username=?",(username,))
    conn.commit()
    conn.close()
    return redirect("/admin")

if __name__=="__main__":
    app.run(debug=True)
    
@app.route("/download_report")
def download_report():

    if not is_logged_in():
       return redirect("/login")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT 
        SUM(CASE WHEN prediction='REAL' THEN 1 ELSE 0 END),
        SUM(CASE WHEN prediction='FAKE' THEN 1 ELSE 0 END)
        FROM history WHERE username=?
    """, (session["user"],))

    data = cur.fetchone()
    conn.close()

    real = data[0] or 0
    fake = data[1] or 0

    file = create_pdf(session["user"], real, fake)

    return send_file(file, as_attachment=True)
