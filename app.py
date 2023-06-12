import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_cors import CORS
import sqlalchemy
from models import setup_db, db, Task, User 
from forms import TaskForm, RegistrationForm, LoginForm



def create_app():
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    setup_db(app, bcrypt)
    CORS(app)
    

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    """def create_database():
        with app.app_context():
            db.create_all()
            print("Database created successfully!") """

    ###
    #AUTHENTICATION
    ###

    @login_manager.user_loader
    def load_user(user_id):
            return db.session.get(User, int(user_id))
    

    @app.route('/register', methods=['GET','POST'])
    def register():
        form = RegistrationForm()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))


        return render_template('register.html', form=form) 
    
    @app.route('/login', methods=['GET','POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('index'))
        
        return render_template('login.html', form=form) 
    
    @app.route('/logout', methods=['GET','POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))


    ###
    #Website
    ###

    @app.route('/')
    @login_required
    def index():
        tasks = Task.query.all()
        tasks_json = [task.to_json() for task in tasks]  # Convert Task objects to JSON-serializable dictionaries
        users = User.query.all()
        users_json = [user.to_json() for user in users]  # Convert Task objects to JSON-serializable dictionaries

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(tasks_json)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(users_json)

        print(tasks_json)
        print(tasks)
        return render_template('index.html') 
    
    @app.route('/users')
    @login_required
    def commentsbyuser():
        users = User.query.all()
        users_json = [user.to_json() for user in users]  # Convert Task objects to JSON-serializable dictionaries
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(users_json)

        print(users_json)
        print(users)
        return render_template('comments_by_user.html') 

    @app.route('/create', methods=['POST'])
    @login_required
    def create_task():
        user_input = request.get_json()
        form = TaskForm(data=user_input)
        
        # Validate the form
        if form.validate():
            task = Task(title=form.title.data, user_id = current_user.id)
            db.session.add(task)
            db.session.commit()
            return jsonify(task.to_json())
        
        return redirect(url_for('index'))


    @app.route('/delete', methods=['POST'])
    @login_required
    def delete_task():
        task_id = request.get_json().get('id')
        task = Task.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result':'OK'}),200


    @app.route('/complete', methods=['POST'])
    @login_required
    def complete_task():
        task_id = request.get_json().get('id')
        task = Task.query.filter_by(id=task_id).first()
        if task.completed:
            task.completed = False
        elif not task.completed:
            task.completed = True
        db.session.add(task)
        db.session.commit()
        return jsonify({'result':'OK'}),200 
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run()


  
