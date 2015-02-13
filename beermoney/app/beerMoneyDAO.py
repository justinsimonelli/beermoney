from app import db
from .models import User, CheckIn


def load_user_by_nickname(nickname):
    return User.query.filter_by(nickname=nickname).first()

def load_user_by_email(email):
    return User.query.filter_by(email=email).first()

def saveCheckIn(_location, _drink, _price):
    drank = CheckIn(location = _location, drink=_drink, cost=_price)
     #this is the fastest, most hack way to do this shit.

    db.session.add(drank)
    db.session.commit()

    return drank

def getAllCheckins():
    czechs = CheckIn.query.all()
    return czechs

def registerUser(formData):
    user = User(nickname=formData.username.data,
                email=formData.email.data,
                password=formData.password.data,
                token=None)
    db.session.add(user)
    db.session.commit()

    return user

def registerFoursquareUser(_nickname, _email, _token):
    user = User(nickname=_nickname,
                email=_email,
                password=_token,
                token=_token)
    db.session.add(user)
    db.session.commit()

    return user