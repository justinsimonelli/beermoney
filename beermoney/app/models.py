from app import db

class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(256), index=True)
    drink = db.Column(db.String(256), index=True)
    cost = db.Column(db.String(25), index=True)

    #define a __repr__ (aka toString) so we know that the fuck
    #is being inserted (via debug or console)
