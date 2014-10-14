from app import app
from flask import render_template, request
from app import checkInDAO

@app.route('/')
@app.route('/index')
def index():
    return "hello world!"

@app.route('/checkin')
@app.route('/checkin/')
def checkIt():
    return render_template('checkin.html',
                           title="get drunk. save cash.")

 #make this a GET request for now so we can be lazy and use query params
@app.route('/checkin/drink', methods=['GET'])
@app.route('/checkin/drink/', methods=['GET'])
def saveCheckIn():
    _location = request.args.get('location', '')
    _drink = request.args.get('drink', '')
    _price = request.args.get('price', '')

    _checkin = checkInDAO.saveCheckIn(_location, _drink, _price)
    _allCheckins = checkInDAO.getAllCheckins()

    return render_template('checkinSuccess.html',
                               checkin = _checkin,
                               allCheckins = _allCheckins)