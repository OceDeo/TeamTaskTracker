from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import desc

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:z6014367@localhost/TTT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

                        ##### USERS #####

class Users(db.Model):  # works
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(200), unique = True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'{self.id},{self.username},{self.password}'


class UserRepository:
    def add_user(username, password):
        user = Users(username, password)
        db.session.add(user)
        db.session.commit()
        
    def user_exists_check(new_username):
        if db.session.query(Users).filter(Users.username == new_username).count() == 0:
            pass
        else:
            return False

    def user_list():
        users = db.session.query(Users).all()
        return users 

                        ##### PROJECTS #####

class Projects(db.Model): #works
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200))
    users = db.Column(db.String(200))
    start_date = db.Column(db.String(10))
    deadline = db.Column(db.String(10))

    def __init__(self, project_name, users, start_date, deadline):
        self.project_name = project_name
        self.users = users
        self.start_date = start_date
        self.deadline = deadline
    
    def __repr__(self):
        return f'{self.project_name}, {self.users}, {self.start_date}, {self.deadline}'


class ProjectRepository:
    def create_project(project_name, user, start_date, deadline): # WORKS
        project = Projects(project_name, user, start_date, deadline)
        db.session.add(project)
        db.session.commit()

    def add_user_to_project(project_id, user_id): # WORKS
        project = Projects.query.filter_by(id = project_id).first()
        users_list = project.users.split(',')
        if str(user_id) in users_list:
            return None
        else:
            project.users += f',{user_id}'
            db.session.add(project)
            db.session.commit()

    def remove_user_from_project(project_id, user_id):
        project = Projects.query.filter_by(id = project_id).first()
        users_list = project.users.split(',')
        if str(user_id) in users_list:
            print(users_list)
            users_list.remove(f'{user_id}')
            users = ','.join(users_list)
            project.users = users
            db.session.add(project)
            db.session.commit()
        else:
            return None

    def fetch_project(project_id):
        project = Projects.query.filter_by(id = project_id).first()
        return project

    def user_projects(user_id):
        projects = Projects.query.filter(Projects.users.contains(str(user_id))).order_by(desc(Projects.id)).all()
        return projects

    def edit_project(project_id, project_name, start_date, deadline):
        project = Projects.query.filter_by(id = project_id).first()
        if project_name != None:
            project.project_name = project_name
        if start_date != None:
            project.start_date = start_date
        if deadline != None:
            project.deadline = deadline
        db.session.add(project)
        db.session.commit()

    def delete_project(project_id):
        project = Projects.query.filter_by(id=project_id).first()
        db.session.delete(project)
        db.session.commit()

                        ##### TASKS #####

class Tasks(db.Model): # works
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(200))
    task = db.Column(db.String(5000))
    task_status = db.Column(db.Boolean, default = False)
    
    def __init__(self, project, task, task_status = False):
        self.project = project
        self.task = task
        self.task_status = task_status

    def __repr__(self):
        return f'<<{self.project} | {self.task} | {self.task_status}>>'


class TaskRepository:
    def add_task(project_id, task): # works
        task = Tasks(project_id, task)
        db.session.add(task)
        db.session.commit()
        return task

    def task_status(task_id): # works
        task = Tasks.query.get(task_id)
        task.task_status = (not task.task_status)
        db.session.commit()

    def tasks_project(project_id):
        return Tasks.query.filter(Tasks.project.contains(str(project_id))).order_by(desc(Tasks.id)).all()

    def delete_task(task_id):
        task = Tasks.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()

