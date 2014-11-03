from app import db
from flask_login import unicode


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(100))
    dateInserted = db.Column(db.DateTime)
    dateUpdated = db.Column(db.DateTime)
    checkins = db.relationship('CheckIn', backref='drinker', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.nickname)  # python 2
        except NameError:
            return str(self.nickname)  # python 3
    def __repr__(self):
        return '<User %r>' % (self.nickname)

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