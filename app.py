from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Task
from forms import TaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True  # Disable debugging
db.init_app(app)



class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<ToDo ID: {self.id}, Description: {self.name}>'


def create_database():
    with app.app_context():
      db.create_all()
      print("Database created successfully!")


@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
      'description': todo.description
    })


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
