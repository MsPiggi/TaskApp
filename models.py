from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime
from app import db





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

