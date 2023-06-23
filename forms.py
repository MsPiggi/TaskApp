from models import User
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired



class TaskForm(FlaskForm):
    title = StringField('Aufgabe', validators=[DataRequired()], render_kw={'placeholder':'To Do'})
    due_to = DateField('Fällig am')
    gurki = SelectField('Gurki', choices = [], validators=[DataRequired()])
    submit = SubmitField('Neues Todo')
    
        

    

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

