from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, RegisterForm
from .models import User
from app import app, db, lm, beerMoneyDAO, f_client, login_serializer
from .utils import flash_errors
from itsdangerous import BadSignature, BadData

@app.before_request
def before_request():
    g.user = current_user
    #g.user is None
    #if session['user_id'] is not None:
        #g.user = User.query.get(session['user_id'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@lm.token_loader
def load_token(token):
    try:
        max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
        payload = login_serializer.loads(token, max_age)

        #print('user=' + payload[0])

        user = User.query.get(payload[0])

        if user and payload[1] == user.token:
            return user

    except BadSignature, e:
        print('exception occurred=' + e.message)

    return None

@app.route('/')
@login_required
def index():
    return redirect(request.args.get('next') or url_for('checkin'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(request.args.get('next') or url_for('checkin'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate():
            user = beerMoneyDAO.load_user_by_nickname(form.username.data.lower())
            login_user(user, remember=True)
            ###########################
            #this might not be safe!!!
            ###########################
            session['nickname'] = user.nickname
            return redirect(request.args.get('next') or url_for('checkin'))

        else:
            flash('Hmm..you sure that login info is correct? \n'
                  'Try entering your username and password again.')

    else:
        flash('Looks like you need to sign in again. Do so below!')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           foursquare=f_client.oauth.auth_url())

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'GET':
        return render_template('register.html',
                           title='Register',
                           form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            usr = User.query.filter_by(nickname=form.username.data, password=form.password.data).first()
            if (usr is not None):
                flash('That username has already been taken! Try another one..')
            else:
                user = beerMoneyDAO.registerUser(form)
                login_user(user, remember=True)
                return redirect(url_for('checkin'))
        else:
            flash_errors(form)

    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return render_template('logout.html',
                           title='Sign Out')

################################################
########### FUN STUFF!! ########################
################################################

@app.route('/oauth/foursquare')
@app.route('/oauth/foursquare/')
def foursquare_auth():
    code = request.args.get('code')
    access_token = f_client.oauth.get_token(code)
    f_client.set_access_token(access_token)
    f_user = f_client.users()
    user = User.query.filter_by(email=f_user['user']['contact']['email']).first()
    if f_user is not None and user is None:
        user = beerMoneyDAO.registerFoursquareUser(f_user['user']['firstName'],
                                                   f_user['user']['contact']['email'],
                                                   access_token)

    else:
        user = beerMoneyDAO.load_user_by_email(f_user['user']['contact']['email'])
        #if user.token != access_token:
            #flash('Looks like we couldn''t find you! Try re-authenticating below')
            #return redirect(url_for('login'))
        #else:
        login_user(user, remember=True)

    return redirect(request.args.get('next') or url_for('checkin'))

@app.route('/foursquare/search/', methods=['GET', 'POST'])
@login_required
def foursquare_search():
    if request.method == 'POST':
        print('inside POST')

    elif request.method == 'GET':
        f_user = f_client.users()
        venues = f_client.venues.search(params={
            'near': 'avon lake,ohio',
            'query': request.args.get('q'),
            'limit': 25
        })

        venue_dict = {}

        #for venue in venues:
         #   venue_data = {'venue': {
          #      'id': venue.id,
           #     'name': venue.name,
            #    'location': venue.location
            #}}
            #venue_dict.update(venue_data)


        #return json.dumps(venue_dict)
        return "still working on it"

############################################
#MAKE THIS login_required again!!!!#########
############################################

@app.route('/beer-lists/')
@login_required
def viewLists():
    return render_template('beerLists.html',
                            user=g.user)

@app.route('/beer-lists/add/', methods=['POST'])
@login_required
def addBeerList():
    print('adding beer')


@app.route('/checkin/')
@login_required
def checkin():
    return render_template('checkin.html',
                           title="get drunk. save cash.",
                           user=g.user)

 #make this a GET request for now so we can be lazy and use query params
@app.route('/checkin/drink/', methods=['GET', 'POST'])
@login_required
def saveCheckIn():
    #try request.get_json() instead?
    _location = request.args.get('location', None)
    _drink = request.args.get('drink', None)
    _price = request.args.get('price', None)

    _checkin = beerMoneyDAO.saveCheckIn(_location, _drink, _price)
    _allCheckins = beerMoneyDAO.getAllCheckins()

    return render_template('checkinSuccess.html', checkin = _checkin, allCheckins = _allCheckins)