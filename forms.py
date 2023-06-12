from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User

class TaskForm(Form):
    title = StringField('title', validators=[DataRequired()])
    

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Password'})
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'EMail'})
    submit = SubmitField('Register')

    def validate_username(self,username):
        existing_user_name = User.query.filter_by(username=username.data).first()
        if existing_user_name:
            raise ValidationError('Username already exists')
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Password'})
    submit = SubmitField('Login')

