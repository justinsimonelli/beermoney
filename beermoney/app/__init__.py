from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from itsdangerous import URLSafeTimedSerializer
import foursquare

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.session_protection = "strong"
login_serializer = URLSafeTimedSerializer(app.secret_key)
#lm.login_message = u""

# Construct the client object
f_client = foursquare.Foursquare(
    client_id='IMJSKYESMU5NFSRL31MO1GGVBQRK5JZOFN1SLAN3FF01CBWL',
    client_secret='NNF5W5AKOXGJQALG31O3YIMFEN5JSHR0N2Z1XYQKY134ZIUR',
    redirect_uri='http://localhost:5000/oauth/foursquare/')

from app import routes, models

