import os
from flask import Flask
from flask import render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import Task
from forms import TaskForm

app = Flask(__name__)
if 'DATABASE_URL' in os.environ:
    # Heroku database URL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    # Local database URL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/example'


#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yjtslemzwfespj:ef2c9832eebf12f4d8e0c264c677d2034c435dd3f27ecc6ca6b43426a73750cb@ec2-34-197-91-131.compute-1.amazonaws.com:5432/d28gb5rnh8v90u'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True  # Enable/Disable debugging

db.init_app(app)


def create_database():
    with app.app_context():
      db.create_all()
      print("Database created successfully!")


@app.route('/')
def index():
  tasks = Task.query.all()

  if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      return jsonify(tasks)

  return render_template('index.html') 


@app.route('/create', methods=['POST'])
def create_task():
    user_input = request.get_json()
    form = TaskForm(data=user_input)
    
    # Validate the form
    if form.validate():
      task = Task(title=form.title.data)
      db.session.add(task)
      db.session.commit()
      return jsonify(task)
    
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = request.get_json().get('id')
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result':'OK'}),200


@app.route('/complete', methods=['POST'])
def complete_task():
    task_id = request.get_json().get('id')
    task = Task.query.filter_by(id=task_id).first()
    task.completed = True
    db.session.add(task)
    db.session.commit()
    return jsonify({'result':'OK'}),200 


if __name__ == '__main__':
  create_database()
  app.run()
