from app import db, login_serializer
import flask_login
from werkzeug import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(100))
    token = db.Column(db.String(150))
    #dateInserted = db.Column(db.DateTime)
    #dateUpdated = db.Column(db.DateTime)
    #checkins = db.relationship('CheckIn', backref='drinker', lazy='dynamic')

    def __init__(self, nickname, email, password, token):
        self.nickname = nickname.lower()
        self.email = email.lower()
        self.set_password(password)
        self.token = self.get_auth_token()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_auth_token(self):
        data = [str(self.id), self.token]
        return login_serializer.dumps(data)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class List(db.Model):
    __tablename__ = 'beer_lists'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), index=True, unique=True)
    dateIntended = db.Column("date_intended", db.DateTime)
    dateInserted = db.Column("date_inserted", db.DateTime)
    dateUpdated = db.Column("date_updated", db.DateTime)

class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.Integer, db.ForeignKey('venue.id'))
    location = db.Column(db.String(256), index=True)
    drink = db.Column(db.String(256), index=True)
    cost = db.Column(db.String(25), index=True)
    dateInserted = db.Column(db.DateTime)
    dateUpdated = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


    @property
    def __repr__(self):
        return '<CheckIn id=%r, drink=%r>' % (self.id, self.drink)

class Venue(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(256), index=True)
     #adress, city, state, zip, lat, long?
     checkins = db.relationship('CheckIn', backref='checkin', lazy='dynamic')