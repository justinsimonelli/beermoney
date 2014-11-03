from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User
from app import app, db, checkInDAO, db, lm
from .utils import flash_errors

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(nickname):
    return User.query.filter_by(nickname=nickname).first()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    form = LoginForm()
    return render_template('checkin.html',
                           title='Sign In',
                           user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("inside login")
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('checkin'))
    form = LoginForm()
    print("validate - " + str(form.validate_on_submit()))
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        usr = User.query.filter_by(nickname=form.username.data).first()
        if (usr is not None):
            login_user(usr)
            return redirect(request.args.get("next") or url_for("login"))
        else:
            flash('Are you drunk already? Try that username and password again. Or try putting in your bank account number.')
    else:
        flash_errors(form)
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html',
                           title='Sign Out')

@app.route('/checkin')
@app.route('/checkin/')
@login_required
def checkIt():
    return render_template('checkin.html',
                           title="get drunk. save cash.")

 #make this a GET request for now so we can be lazy and use query params
@app.route('/checkin/drink', methods=['GET', 'POST'])
@app.route('/checkin/drink/', methods=['GET', 'POST'])
@login_required
def saveCheckIn():
    #try request.get_json() instead?
    _location = request.args.get('location', None)
    _drink = request.args.get('drink', None)
    _price = request.args.get('price', None)

    _checkin = checkInDAO.saveCheckIn(_location, _drink, _price)
    _allCheckins = checkInDAO.getAllCheckins()

    return render_template('checkinSuccess.html', checkin = _checkin, allCheckins = _allCheckins)