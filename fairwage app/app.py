from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import numpy as np

app = Flask(__name__)
app.secret_key="fairwage_secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ---------------- DATABASE ----------------

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    password=db.Column(db.String(100))

class Report(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    issue=db.Column(db.String(500))

# ---------------- SALARY DATA ----------------

salary_db = {

"mumbai": {
"construction": 22000,
"factory": 20000,
"electrician": 25000,
"delivery": 18000,
"driver": 22000,
"data_entry": 21000,
"accountant": 35000,
"developer": 60000,
"security": 17000,
"shop_worker": 18000,
"farm_worker": 16000
},

"pune": {
"construction": 20000,
"factory": 18000,
"electrician": 23000,
"delivery": 16000,
"driver": 20000,
"data_entry": 20000,
"accountant": 32000,
"developer": 55000,
"security": 16000,
"shop_worker": 17000,
"farm_worker": 15000
},

"kolhapur": {
"construction": 18000,
"factory": 16000,
"electrician": 21000,
"delivery": 14000,
"driver": 18000,
"data_entry": 18000,
"accountant": 28000,
"developer": 45000,
"security": 15000,
"shop_worker": 16000,
"farm_worker": 14000
}

}


# ---------------- AI PREDICTION DEMO ----------------

def predict_salary(exp):
    base=15000
    return int(base + exp*2500 + np.random.randint(-2000,2000))

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        u=User(username=request.form["username"],password=request.form["password"])
        db.session.add(u)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=User.query.filter_by(
        username=request.form["username"],
        password=request.form["password"]
        ).first()
        if u:
            session["user"]=u.username
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

@app.route("/calculator",methods=["GET","POST"])
def calculator():
    result=None
    if request.method=="POST":
        city=request.form["city"]
        job=request.form["job"]
        salary=int(request.form["salary"])

        fair=salary_db.get(city,{}).get(job,15000)
        status="Fair" if salary>=fair else "Underpaid ⚠"

        result=f"Fair Wage ₹{fair} | Status: {status}"

    return render_template("calculator.html",result=result)

@app.route("/compare",methods=["GET","POST"])
def compare():
    result=None
    if request.method=="POST":
        city=request.form["city"]
        job=request.form["job"]
        fair=salary_db.get(city,{}).get(job,15000)
        result=f"Average Wage ₹{fair}"

    return render_template("compare.html",result=result)

@app.route("/report",methods=["GET","POST"])
def report():
    msg=None
    if request.method=="POST":
        r=Report(issue=request.form["issue"])
        db.session.add(r)
        db.session.commit()
        msg="Anonymous Report Submitted ✅"
    return render_template("report.html",msg=msg)

@app.route("/ai_predict",methods=["GET","POST"])
def ai_predict():
    result=None
    if request.method=="POST":
        exp=int(request.form["exp"])
        result=f"Predicted Fair Wage ₹{predict_salary(exp)}"
    return render_template("ai_predict.html",result=result)

@app.route("/analytics")
def analytics():
    data=[18000,16000,14000]
    cities=["Mumbai","Pune","Kolhapur"]
    return render_template("analytics.html",data=data,cities=cities)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- ADMIN ROUTE ----------------

@app.route("/admin")
def admin():

    if "user" not in session:
        return redirect("/login")

    users = User.query.all()
    reports = Report.query.all()

    total_users = len(users)
    total_reports = len(reports)

    return render_template(
        "admin.html",
        users=users,
        reports=reports,
        total_users=total_users,
        total_reports=total_reports
    )
@app.route("/delete_user/<int:id>")
def delete_user(id):

    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect("/admin")


@app.route("/delete_report/<int:id>")
def delete_report(id):

    report = Report.query.get(id)
    if report:
        db.session.delete(report)
        db.session.commit()

    return redirect("/admin")



# ---------------- RUN APP ----------------

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
