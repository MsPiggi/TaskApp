from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_cors import CORS
import sqlalchemy
from models import setup_db, db, Task, User 
from forms import TaskForm, RegistrationForm, LoginForm
from flask_migrate import Migrate



def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    #app.config.from_object("config.DevelopmentConfig")

    """   print(app.config["ENV"])
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    elif app.config["ENV"] == "develoment":
        app.config.from_object("config.DevelopmentConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("config.TestingConfig") """
    
    
    
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

        if form.validate():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
            new_user = User(username=form.username.data, password=hashed_password, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Der User wurde erfolgreich angelegt")
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
    #Team
    ###

    @app.route('/users/delete/<int:id>', methods=['GET'])
    @login_required
    def delete_user(id):
        user_to_delete = User.query.get_or_404(id)
        print(user_to_delete)
        form = RegistrationForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User erfolgreich gelöscht")
            
            team = User.query.all()
            users_json = [user.to_json() for user in team]  # Convert Task objects to JSON-serializable dictionaries
            return render_template('team.html', users=users_json, form=form) 
        
        except:
            flash("Es gab ein Problem beim löschen")
            team = User.query.all()
            users_json = [user.to_json() for user in team]  # Convert Task objects to JSON-serializable dictionaries
            return render_template('team.html', users=users_json, form=form) 


    @app.route('/users/create', methods=['POST','GET'])
    @login_required
    def create_user():
        form = RegistrationForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data, email=form.email.data).first()
            if user is None:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
                new_user = User(username=form.username.data, password=hashed_password, email=form.email.data)
                db.session.add(new_user)
                db.session.commit()
                flash("Der User wurde erfolgreich angelegt")
            else:
                flash("Der User existiert bereits")

        team = User.query.all()
        users_json = [user.to_json() for user in team]  # Convert Task objects to JSON-serializable dictionaries
        return render_template('team.html', users=users_json, form=form) 
    

    @app.route('/users', methods=['POST','GET'])
    @login_required
    def team():
        form = RegistrationForm()
        team = User.query.all()
        users_json = [user.to_json() for user in team]  # Convert Task objects to JSON-serializable dictionaries
        return render_template('team.html', users=users_json, form=form) 
    
    ###
    #User Profile
    ###

    @app.route('/user', methods=['POST','GET'])
    @login_required
    def user_profile():
        username = User.query.filter_by(id=current_user.id).first().to_json().get('username')
        assigned_tasks = Task.get_assigned_tasks(username)
        favourite_gurki = Task.get_favourite_gurki(current_user.id)
        ammount_open_user_tasks = len(Task.get_open_tasks(current_user.id))
        ammount_completed_user_tasks = len(Task.get_completed_tasks(current_user.id))

        """ ammount_open_user_tasks = len(user_tasks.filter(completed=False))
        ammount_completed_user_tasks = len(user_tasks.filter(completed=True)) """
        return render_template('user_profile.html', 
                               user=current_user, 
                               tasks = assigned_tasks,
                               ammount_open_user_tasks = ammount_open_user_tasks,
                               ammount_completed_user_tasks = ammount_completed_user_tasks,
                               favourite_gurki = favourite_gurki
                               ) 



    ###
    #TASK
    ###

    @app.route('/')
    @login_required
    def index():
        form = TaskForm()
        team = User.query.all()
        form.gurki.choices = [user.to_json().get('username') for user in team]
        tasks = Task.query.all()
        #tasks_json = [task.to_json() for task in tasks]  # Convert Task objects to JSON-serializable dictionaries
        users = User.query.all()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(tasks)
        
        
        print(tasks)
        print(app.config)
        return render_template('index.html', tasks = tasks, user = current_user, users = users, form = form ) 
    

    @app.route('/task/create', methods=['POST'])
    @login_required
    def create_task():
        form = TaskForm()
        team = User.query.all()
        form.gurki.choices = [user.to_json().get('username') for user in team]
        # Validate the form
        if form.validate_on_submit():
            task = Task(title=form.title.data, due_to = form.due_to.data, user_id = current_user.id, gurki = form.gurki.data)
            db.session.add(task)
            db.session.commit()
            form.title.data = ''
            form.due_to.data = ''
            form.gurki.data = ''

        
        tasks = Task.query.all()

        return render_template('index.html', tasks = tasks, user = current_user, form = form ) 


    @app.route('/task/delete/<int:id>', methods=['GET','POST'])
    @login_required
    def delete_task(id):
        task_id = request.get_json().get('id')
        task = Task.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result':'OK'}),200


    @app.route('/task/complete', methods=['POST'])
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
    

    ###
    #Error Handler 
    ###
    
    #Invalid URL
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
    
    #Internal Server Error
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template("404.html"), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


  
  #Jinja2 filters
    #safe
    #capitalize
    #lower
    #upper
    #title
    #trim
    #striptags