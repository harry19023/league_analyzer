from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app import app
from modules.league_parsing import checkLeagueInfo, loadLeague
from modules.user import create_user, load_user
from modules.forms import RegisterForm, LoginForm, LeagueIDForm


@app.route("/", methods=["GET", "POST"])
def index():
    form = LeagueIDForm()
    if form.validate_on_submit():
        leagueID = str(form.leagueID.data)
        checkLeagueInfo(leagueID)
        league = loadLeague(leagueID)
        return render_template("main_page.html", league=league, form=form)
    return render_template("main_page.html", form=form, league=None)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.username.data)
        login_user(user)
        return redirect(url_for("index"))
    return render_template("login_page.html", form=form)


@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = create_user(form.username.data, form.password.data)
        login_user(user)
        flash("Thanks for creating an account!")
        return redirect(url_for('index'))
    return render_template("register_page.html", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
