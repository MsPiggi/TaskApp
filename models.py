import os
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime
from flask_migrate import Migrate


db = SQLAlchemy()

def setup_db(app, bcrypt):
    migrate = Migrate(app,db)

    if 'DATABASE_URL' in os.environ:
        # Heroku database URL
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yjtslemzwfespj:ef2c9832eebf12f4d8e0c264c677d2034c435dd3f27ecc6ca6b43426a73750cb@ec2-34-197-91-131.compute-1.amazonaws.com:5432/d28gb5rnh8v90u' #os.environ['DATABASE_URL']
    else:
        # Local database URL
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/example'


    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yjtslemzwfespj:ef2c9832eebf12f4d8e0c264c677d2034c435dd3f27ecc6ca6b43426a73750cb@ec2-34-197-91-131.compute-1.amazonaws.com:5432/d28gb5rnh8v90u'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/example'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SECRET_KEY'] = 'thisisasecretkey'
    #app.config['DEBUG'] = True
    db.app = app
    db.init_app(app)
    
    
    #db_drop_and_create(app, bcrypt)
    

#def db_drop_and_create(app, bcrypt):
    #with app.app_context():
        # db.drop_all()
        #db.create_all()
        #insert_basic_data(bcrypt)


def insert_basic_data(bcrypt):
    existing_user = User.query.filter_by(username='test').first()
    if not existing_user:
        # Create the user "test" with the password "test"
        user = User(username='test', password=bcrypt.generate_password_hash('test').decode('utf8'), email='test@example.com')
        db.session.add(user)
        db.session.commit()

        # Add tasks for the user if they don't exist
        tasks = Task.query.filter_by(user_id=user.id).first()
        if not tasks:
            task1 = Task(title="Task 1", date=datetime.now(), completed=False, user_id=user.id)
            db.session.add(task1)

            task2 = Task(title="Task 2", date=datetime.now(), completed=True, user_id=user.id)
            db.session.add(task2)

            db.session.commit()

    elif existing_user: 
        # User already exists, so add tasks if they don't exist
        # Add tasks for the user if they don't exist
        tasks = Task.query.filter_by(user_id=existing_user.id).first()
        if not tasks:
            task1 = Task(title="Task 1", date=datetime.now(), completed=False, user_id=user.id)
            db.session.add(task1)

            task2 = Task(title="Task 2", date=datetime.now(), completed=True, user_id=user.id)
            db.session.add(task2)

            db.session.commit()
    

class User(UserMixin, db.Model):
    id: int
    username: str
    email: str
    password: str
      

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(240), nullable=False)
    tasks = db.relationship('Task', backref='user')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
   

    def get_id(self):
        return str(self.id)
    
    def to_json(self):        
        return {"id": self.id,
                "username": self.username,
                "email": self.email}

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          


class Task(db.Model):

    id: int
    title: str
    date: datetime  
    completed: bool
    user_id: int
    
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date = db.Column(db.DateTime(), default=datetime.now())
    due_to = db.Column(db.DateTime())
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
    """ def to_json(self):
        return {
            "id":self.id,
            "title": self.title,
            "date": self.date.isoformat(),
            "completed": self.completed,
            "user_id": self.user_id,
            "due_to": self.date.isoformat(),
        } """

    def __repr__(self):
        return f'<Task id: {self.id} - {self.title}>'

