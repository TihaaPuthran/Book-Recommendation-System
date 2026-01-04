from flask import render_template, redirect, url_for, flash, request
from Main import app, db, bcrypt
from Main.recomm import recom
from flask_login import login_user, logout_user, login_required, current_user
from Main.models import User
from Main.form import RegistrationForm, LoginForm, BookForm


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("recommender"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/recommender", methods=["GET", "POST"])
@login_required
def recommender():
    form = BookForm()
    recommendations = []

    if form.validate_on_submit():
        book = form.bookname.data
        recommendations = recom(book)

    return render_template(
        "recommender.html",
        form=form,
        recommendations=recommendations
    )

