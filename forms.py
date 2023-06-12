from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from models import User

class TaskForm(Form):
    title = StringField('title', validators=[DataRequired()])

    

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Password'})
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'EMail'})
    submit = SubmitField('Hinzufügen')

    def validate_unique_username_and_mail(self,username, email):
        existing_user_name = User.query.filter_by(username=username.data).first()
        if existing_user_name:
            raise ValidationError('Username already exists')
        
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('Email already exists')
    

        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Username'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder':'Password'})
    submit = SubmitField('Login')

