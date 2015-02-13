from flask.ext.wtf import Form
from app import models
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(message=(u'Doesn''t really looks like a valid username..'))])
    password = PasswordField('password', validators=[DataRequired(message=(u'Check that password again..'))])
    remember_me = BooleanField('remember_me', default=False)

    def validate(self):
        if not Form.validate(self):
            return False
        user = models.User.query.filter_by(nickname=self.username.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.username.errors.append("Invalid e-mail or password")
            return False


class RegisterForm(Form):
    email = StringField('email',
                        validators=[
                            DataRequired(message=(u'Need to enter an email address!')),
                            Email()])
    username = StringField('username', validators=[DataRequired(message=(u'Need to enter a username!'))])
    password = PasswordField('password', validators=[DataRequired(message=(u'Looks like you forgot to add a pasword.'))])