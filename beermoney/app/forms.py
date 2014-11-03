from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(message=(u'Doesn''t really looks like a valid username..'))])
    password = StringField('password', validators=[DataRequired(message=(u'You forgot to enter your password!'))])
    remember_me = BooleanField('remember_me', default=False)