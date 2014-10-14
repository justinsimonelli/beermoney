from app import app
from flask import render_template, request, jsonify
from app import checkInDAO
import jsonpickle

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
@app.route('/checkin/drink', methods=['GET', 'POST'])
@app.route('/checkin/drink/', methods=['GET', 'POST'])
def saveCheckIn():
    #try request.get_json() instead?
    _location = request.args.get('location', None)
    _drink = request.args.get('drink', None)
    _price = request.args.get('price', None)

    _checkin = checkInDAO.saveCheckIn(_location, _drink, _price)
    _allCheckins = checkInDAO.getAllCheckins()

    return render_template('checkinSuccess.html', checkin = _checkin, allCheckins = _allCheckins)