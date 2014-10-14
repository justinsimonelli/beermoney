from app import db, models

def saveCheckIn(_location, _drink, _price):
    drank = models.CheckIn(location = _location, drink=_drink, cost=_price)
     #this is the fastest, most hack way to do this shit.
     #kinda drunk and need to read this doc later, but fuck it for now


    ##haha buttfuckit. get it. GET IT!?
    db.session.add(drank)
    db.session.commit()

    return drank

def getAllCheckins():
    czechs = models.CheckIn.query.all()
    return czechs