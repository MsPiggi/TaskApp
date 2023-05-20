import os
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime


db = SQLAlchemy()

def setup_db(app):
    if 'DATABASE_URL' in os.environ:
        # Heroku database URL
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yjtslemzwfespj:ef2c9832eebf12f4d8e0c264c677d2034c435dd3f27ecc6ca6b43426a73750cb@ec2-34-197-91-131.compute-1.amazonaws.com:5432/d28gb5rnh8v90u' #os.environ['DATABASE_URL']
    else:
        # Local database URL
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/example'


    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yjtslemzwfespj:ef2c9832eebf12f4d8e0c264c677d2034c435dd3f27ecc6ca6b43426a73750cb@ec2-34-197-91-131.compute-1.amazonaws.com:5432/d28gb5rnh8v90u'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/example'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True  # Enable/Disable debugging
    db.app = app
    db.init_app(app)
    db_drop_and_create(app)
    

def db_drop_and_create(app):
    with app.app_context():
        # db.drop_all()
        db.create_all()
        insert_basic_data()


def insert_basic_data():
    task1 = Task(title="Task 1", date=datetime.now(), completed=False)
    db.session.add(task1)
    
    task2 = Task(title="Task 2", date=datetime.now(), completed=True)
    db.session.add(task2)
    
    db.session.commit()



@dataclass
class Task(db.Model):

    id: int
    title: str
    date: datetime  
    completed: bool
    
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date = db.Column(db.DateTime(), default=datetime.now())
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def __repr__(self):
        return f'<Task id: {self.id} - {self.title}>'

