from datetime import datetime
from flask import Flask, render_template, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import create_session, query
from werkzeug.utils import redirect
import random


app = Flask(__name__)
app.secret_key = "anudeep"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Data(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    name = db.Column(db.String(100))
    account_number = db.Column(db.String(15))
    email = db.Column(db.String(100))
    number = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    profession = db.Column(db.String(20))
    salary = db.Column(db.String(25))
    account = db.Column(db.String(15))
    password = db.Column(db.String(100))
    created = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, fname, sname, email, number, gender, dob, profession, salary, account, password):
        self.fname = fname
        self.sname = sname
        self.name = fname + " " + sname
        self.account_number = str(random.randint(1000000000, 9000000000))
        self.email = email
        self.number = number
        self.gender = gender
        self.dob = dob
        self.profession = profession
        self.salary = salary
        self.account = account
        self.password = password



class Transactions(db.Model):
    _time = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(50))
    email = db.Column(db.String(50))
    type = db.Column(db.String(50))
    money = db.Column(db.String(50))
    avail_money = db.Column(db.String(50))
    time = db.Column(db.DateTime, default = datetime.utcnow)
    

    def __init__(self, user, email, type, money, avail_money):
        self.user = user
        self.email = email
        self.type = type
        self.money = money
        self.avail_money = avail_money


    # def __repr__(self) -> str:
    #     return self.fname


class Admin(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    name = db.Column(db.String(100))
    office_id = db.Column(db.String(100))
    email = db.Column(db.String(100))
    number = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    branch = db.Column(db.String(100))
    password = db.Column(db.String(100))
    created = db.Column(db.DateTime, default = datetime.utcnow)


    def __init__(self, fname, sname, office_id, email, number, gender, dob, branch, password):
        self.fname = fname
        self.sname = sname
        self.name = fname + " " + sname
        self.office_id = office_id
        self.email = email
        self.number = number
        self.gender = gender
        self.dob = dob
        self.branch = branch
        self.password = password





@app.route("/")
def index():
    return render_template("index.html")



@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":

        found = Data.query.filter_by(email = request.form["email"]).first()
        if found:
            flash("User already exists")
            return render_template("signup1.html")

        for key in request.form:
            session[key] = request.form[key]

        fname = session['Fname']
        sname = session['Lname']
        email = session['email']
        number = session['number']
        gender = session['gender']
        dob = session['dob']
        profession = session['profession']
        salary = session['salary']
        account = session['A_type']
        password = session['password']


        usr = Data(fname = fname, sname = sname, email = email, number = number, gender = gender, dob = dob, profession = profession, salary = salary, account = account, password = password)

        # usr = Data()

        db.session.add(usr)

        transaction = Transactions(request.form["Fname"]+" "+request.form["Lname"], request.form["email"], "Account Creation", "0", "0")
        
        db.session.add(transaction)

        db.session.commit()

        return redirect(url_for("login"))
    else:
        return render_template("signup1.html")





@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        found = Data.query.filter_by(email = email).first()
        if found:
            if password == found.password:
                session["email"] = found.email
                session["account_number"] = found.account_number
                return redirect(url_for("home"))
            else:
                flash("Wrong password")
        else:
            flash("Email not found")
    return render_template("login1.html")


@app.route("/home")
def home():
    try:
        if session["email"]:
            transactions = Transactions.query.filter_by(email = session["email"]).all()
            return render_template("home.html", session = session, transactions = transactions)
    except:
        return redirect(url_for("login"))


# @app.route("/withdraw", methods = ["GET, POST"])
# def withdraw():
    # if request.method == "POST":
    #     amount = str(request.form["amount"])
    #     amount_re = str(request.form["amount_re"])

    #     if amount != amount_re:
    #         flash("re enter amount properly")
    #         return render_template("deposit.html")

    #     user = Data.query.filter_by(email = session["email"]).first()
    #     bal = Transactions.query.filter_by(email = session["email"]).all()[-1]
    #     if int(bal.avail_money) < int(amount):
    #         flash("You dont have enough money")
    #         return render_template("withdraw.html")

    #     transaction = Transactions(user.name, user.email, "withdraw", amount, str(int(bal.avail_money) - int(amount)))

    #     db.session.add(transaction)
    #     db.session.commit()

    #     flash("sucessfully deposited")

    #     return redirect(url_for("home"))

    # return render_template("withdraw.html")




@app.route("/withdraw", methods = ["GET", "POST"])
def withdraw():
    if request.method == "POST":
        amount = str(request.form["amount"])
        amount_re = str(request.form["amount_re"])

        if amount != amount_re:
            flash("re enter amount properly")
            return render_template("withdraw.html")

        try:        
            user = Data.query.filter_by(email = session["email"]).first()
            bal = Transactions.query.filter_by(email = session["email"]).all()[-1]
        except:
            return redirect(url_for("login"))
        if int(bal.avail_money) < int(amount):
            flash("You dont have enough money")
            return render_template("withdraw.html")

        transaction = Transactions(user.name, user.email, "withdraw", amount, str(int(bal.avail_money) - int(amount)))

        db.session.add(transaction)
        db.session.commit()

        flash("sucessfully withdrawn")

        return redirect(url_for("home"))
    return render_template("withdraw.html")


@app.route("/deposit", methods = ["GET", "POST"])
def deposit():
    if request.method == "POST":
        amount = str(request.form["amount"])
        amount_re = str(request.form["amount_re"])

        if amount != amount_re:
            flash("re enter amount properly")
            return render_template("deposit.html")

        try:
            user = Data.query.filter_by(email = session["email"]).first()
            bal = Transactions.query.filter_by(email = session["email"]).all()[-1]
        except:
            return redirect(url_for("login"))

            
        transaction = Transactions(user.name, user.email, "deposit", amount, str(int(bal.avail_money) + int(amount)))

        db.session.add(transaction)
        db.session.commit()

        flash("sucessfully deposited")

        return redirect(url_for("home"))

    return render_template("deposit.html")



@app.route("/admin_register", methods = ["GET", "POST"])
def admin_register():
    if request.method == "POST":

        if request.form["password"] != request.form["password_re"]:
            flash("Wrong password")
            return render_template("signup2.html")

        for key in request.form:
            session[key] = request.form[key]

        admin = Admin(fname = session["Fname"], sname = session["Lname"], office_id = session["office_id"], email = session["email"], number = session["number"], gender = session["gender"], dob = session["dob"], branch = session["branch"], password = session["password"])

        db.session.add(admin)
        db.session.commit()

        return redirect(url_for('admin_login'))

    return render_template("signup2.html")





@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        office_id = request.form["office_id"]
        password = request.form["password"]
        found = Admin.query.filter_by(office_id = office_id).first()
        if found:
            print("yey found")
            if password == found.password:
                flash("login successful")


                session["office_id"] = office_id
                session["name"] = found.name
                session["branch"] = found.branch


                return redirect(url_for("admin_home"))
            else:
                flash("Incorrect password")
                return render_template("login2.html")
        else:
            flash("Id not found")
            return render_template("login2.html")

    return render_template("login2.html")








@app.route("/admin_home", methods=["GET", "POST"])
def admin_home():
    try:
        if session["office_id"]:
            if request.method == "POST":
                session["email_search"] = request.form["email_search"]
                return redirect(url_for('t'))
            users = Data.query.with_entities(Data.name, Data.email , Data.gender, Data.dob ,Data.account_number).all()
            staff = Admin.query.filter_by(office_id = session["office_id"]).first()
            return render_template("admin_home.html", users = users, staff = staff)
    except:
        return redirect(url_for('admin_login'))




@app.route("/t")
def t():
    transactions = Transactions.query.filter_by(email = session["email_search"]).all()[::-1]
    return render_template("t.html", transactions = transactions)





@app.route("/logout")
def logout():
    session.clear()
    return render_template('index.html')





@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")



@app.route("/about_us")
def about_us():
    return render_template("about_us.html")



@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/services")
def services():
    return render_template("services.html")


if __name__ == "__main__":
    app.run(debug=True)