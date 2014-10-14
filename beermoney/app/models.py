from app import db

class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(256), index=True)
    drink = db.Column(db.String(256), index=True)
    cost = db.Column(db.String(25), index=True)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<CheckIn id=%r, drink=%r>' % (self.id, self.drink)
