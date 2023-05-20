import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from models import setup_db, db, Task 
from forms import TaskForm

def create_app():
    app = Flask(__name__)
    setup_db(app)

    """def create_database():
        with app.app_context():
            db.create_all()
            print("Database created successfully!") """



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
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run()


  
