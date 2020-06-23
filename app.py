import bcrypt
import json

from flask import Flask, render_template, request, session, url_for, redirect, g
from flask_sqlalchemy import SQLAlchemy

import services.users_services as usr_s
import services.projects_services as proj_s

app = Flask(__name__) 

app.secret_key = 'dYIbV9GL3VtVyGWq2tp7hybbwCL3Aebz6T80WjuY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:z6014367@localhost/TTT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_request
def before_request(): # check for logged user/any open session
    g.user = None
    if 'user_id' in session:
        user = usr_s.user_by_id(session['user_id'])
        g.user = user

@app.route('/')
def main_page(): # redirect main page to just login
    return redirect(url_for('login_page'))

@app.route('/login', methods = ['GET', 'POST'])
def login_page(): 
    if request.method == 'POST':
        session.pop('user_id', None) #end any current session
        username = request.form['username'] #get username
        password = request.form['password'].encode('utf-8') # get password and convert to bytes
        check, user = usr_s.validate_login(username, password)
        if check == True:
            session['user_id'] = user.id # set session to user id
            return redirect(url_for('user_dashboard')) #redirect to user dashboard
        else:
            pass #if anything fails refresh page
    return render_template('login.html') 

@app.route('/user_dashboard', methods = ['GET']) #### TO BE EDITED, PROJECTS MOVED TO MY PROJECTS
def user_dashboard():
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page'))
    projects = usr_s.proj_user(g.user.id) ## TO CHANGE IN HTML
    return render_template('user_dashboard.jinja2', projects=projects)

@app.route('/create_user', methods = ['GET', 'POST'])
def new_user_page():
    if not g.user:
        return redirect(url_for('login_page'))
    if request.method == 'POST': 
        username = request.form['username'] # new username
        password = request.form['password'] #new password
        password_re = request.form['password_re'] #repeat password
        usr_s.create_user_func(username, password, password_re) # call create user function and add user to database
        return redirect(url_for('login_page')) # redirect to login page
    return render_template('create_user.html')

@app.route('/user_dashboard/<project_id>', methods = ['GET', 'POST'])
def project_page(project_id):
    if not g.user:
        return redirect(url_for('login_page'))
    project = proj_s.specific_proj(project_id)
    tasks = proj_s.project_tasks(project_id)
    if request.method == 'POST':
        task = request.form['add_task']
        task_status = request.form['task_status']
        task_remove = request.form['remove_task']
        proj_s.create_task(project_id,task)
        return redirect(url_for('project_page', project_id = project_id))
    return render_template('project.html', project = project, proj_tasks=tasks, project_id = project_id)

@app.route('/myprojects', methods = ['GET'])
def my_projects():
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page'))
    projects = usr_s.proj_user(g.user.id)
    return render_template('myprojects.jinja2', projects=projects)

@app.route('/add_project', methods = ['GET', 'POST'])
def add_project():
    if not g.user:
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        name = request.form['project_name']
        start_date = request.form['start_date']
        deadline = request.form['deadline']
        if name == '' or start_date == '' or deadline == '':
            return redirect(url_for('add_project'))
        else:
            proj_s.new_project(name, deadline, start_date, g.user.id)
            return redirect(url_for('my_projects'))
    return render_template('add_project.html')    

@app.route('/edit/<project_id>', methods = ['GET', 'POST'])
def edit_project(project_id):
    if not g.user:
        return redirect(url_for('login_page'))
    current_proj = proj_s.specific_proj(project_id)
    name = current_proj.project_name
    start_date = current_proj.start_date
    deadline = current_proj.deadline
    if request.method == "POST":
        name = request.form['project_name']
        start_date = request.form['start_date']
        deadline = request.form['deadline']
    return render_template('edit_project.html', name = name, start_date = start_date, deadline = deadline)

@app.route('/api/projects/<project_id>/add_task', methods = ['POST'])
def add_new_task(project_id):
    task_data = request.get_json()
    taskName = task_data['name']
    proj_s.create_task(project_id, taskName)
    tasks = proj_s.project_tasks(project_id)
    return render_template('task_list.jinja2', proj_tasks = tasks)

@app.route('/api/projects/<project_id>/delete_task', methods = ['POST'])
def delete_task(project_id):
    task_data = request.get_json()
    taskId = task_data['id']
    proj_s.delete_task(taskId)
    tasks = proj_s.project_tasks(project_id)
    return render_template('task_list.jinja2', proj_tasks = tasks)


@app.route('/logout')
def logout():
    g.user = None
    return redirect(url_for(login_page))

if __name__ == '__main__':
    app.run(debug=True)