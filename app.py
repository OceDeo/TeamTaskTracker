import bcrypt
import json
import time

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
    wrong_pass = ''
    if request.method == 'POST':
        session.pop('user_id', None) #end any current session
        username = request.form['username'] #get username
        password = request.form['password'].encode('utf-8') # get password and convert to bytes
        try: # try to validate login
            check, user = usr_s.validate_login(username, password)
            if check == True:
                session['user_id'] = user.id # set session to user id
                return redirect(url_for('user_dashboard')) #redirect to user dashboard
        except: # if login is incorrect return error message and reload login page
            wrong_pass = "Wrong username or password, please try again."
    return render_template('login.html', wrong_pass = wrong_pass) 

@app.route('/user_dashboard', methods = ['GET'])
def user_dashboard():
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page'))
    elif g.user.id == 3: # if user is admin
        create_user = 'Create User'
    else: #if user is not admin
        create_user = ''
    return render_template('user_dashboard.jinja2', create_user = create_user) # otherwise render userdashboard

@app.route('/create_user', methods = ['GET', 'POST'])
def new_user_page():
    if g.user.id == 3: # if user is admin, grant access
        if request.method == 'POST': 
            username = request.form['username'] # new username
            password = request.form['password'] #new password
            password_re = request.form['password_re'] #repeat password
            usr_s.create_user_func(username, password, password_re) # call create user function and add user to database
            return redirect(url_for('login_page')) # redirect to login page
        return render_template('create_user.html') # if user is admin redirect to create-user page
    else:
        return redirect(url_for('login_page')) # otherwise send back to login

@app.route('/user_dashboard/<project_id>', methods = ['GET', 'POST'])
def project_page(project_id):
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page')) 
    elif g.user.id == 3: # if user is admin
        create_user = 'Create User'
    else: #if user is not admin
        create_user = ''
    project = proj_s.specific_proj(project_id) #fetch project data
    tasks = proj_s.project_tasks(project_id) #fetch project tasks
    tasks_details = proj_s.finished_unfinished(project_id)
    if request.method == 'POST':
        task = request.form['add_task']
        task_status = request.form['task_status']
        task_remove = request.form['remove_task']
        proj_s.create_task(project_id,task) # create new task
        return redirect(url_for('project_page', project_id = project_id)) #return page with project id
    return render_template('project.html', project = project, proj_tasks = tasks, project_id = project_id, create_user = create_user, tasks_details = tasks_details) # return page with project, tasks and id for js to receive

@app.route('/myprojects', methods = ['GET'])
def my_projects():
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page'))
    elif g.user.id == 3: # if user is admin
        create_user = 'Create User'
    else: #if user is not admin
        create_user = ''
    projects = usr_s.proj_user(g.user.id) # fetch projects for specific user
    tasks_details = []
    for project in projects:
        task_details = proj_s.finished_unfinished(project.id)
        tasks_details.append(task_details)
    return render_template('myprojects.jinja2', projects=projects, create_user = create_user, tasks_details = tasks_details)

@app.route('/add_project', methods = ['GET', 'POST'])
def add_project():
    fields = ""
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page'))
    elif g.user.id == 3: # if user is admin
        create_user = 'Create User'
    else: #if user is not admin
        create_user = ''
    if request.method == 'POST':
        name = request.form['project_name']
        start_date = request.form['start_date']
        deadline = request.form['deadline']
        if name == '' or start_date == '' or deadline == '': # check if any fields are empty, if so, reload page
            fields = "Some fields are empty"
            return render_template('add_project.html', fields = fields, create_user = create_user) # render page with fields messagfe
        else:
            proj_s.new_project(name, deadline, start_date, g.user.id)# create project
            return redirect(url_for('my_projects')) #return to my projects page
    return render_template('add_project.html', fields = fields, create_user = create_user)    

@app.route('/edit/<project_id>', methods = ['GET', 'POST']) ##### NEED TO CREATE THIS PAGE######
def edit_project(project_id): 
    if g.user.id != 3:
        return redirect(url_for('login_page'))
    elif g.user.id == 3: # if user is admin
        create_user = 'Create User'
        fields = ""
    project = proj_s.specific_proj(project_id)
    name = project.project_name
    start_date = project.start_date
    deadline = project.deadline
    if request.method == "POST":
        name = request.form['project_name']
        start_date = request.form['start_date']
        deadline = request.form['deadline']
        if name == '':
            name = project.project_name
        if start_date == '':
            start_date = project.start_date
        if deadline == '':
            deadline = project.deadline
        proj_s.edit_proj(project_id, name, start_date, deadline)
        return render_template('edit_project.html', fields = fields, project = project, create_user = create_user, name = name) # render page with fields messagfe
            # create project
    return render_template('edit_project.html', fields = fields, project = project, create_user = create_user, name = name)

@app.route('/api/projects/<project_id>/info_tasks')
def task_info(project_id):
    time.sleep(.1)
    tasks_details = proj_s.finished_unfinished(project_id)
    print(tasks_details)
    return render_template('tasks_info.jinja2', tasks_details = tasks_details)

@app.route('/api/projects/<project_id>/add_task', methods = ['POST'])
def add_new_task(project_id):
    task_data = request.get_json() #get task data from htlm/javascript
    taskName = task_data['name'] # extract task from json data
    proj_s.create_task(project_id, taskName) # create task in database
    tasks = proj_s.project_tasks(project_id) #reload all tasks from databse
    return render_template('task_list.jinja2', proj_tasks = tasks) #return all tasks to the tasks template

@app.route('/api/projects/<project_id>/delete_task', methods = ['POST'])
def delete_task(project_id):
    task_data = request.get_json() #get delete request
    taskId = task_data['id'] # extract task id
    proj_s.delete_task(taskId) # remove task from database
    tasks = proj_s.project_tasks(project_id) #reload tasks from database
    return render_template('task_list.jinja2', proj_tasks = tasks) #return all tasks to tasks template

@app.route('/api/projects/<project_id>/status_task', methods = ['POST'])
def task_status(project_id):
    task_data = request.get_json()
    task_id = task_data['id']
    proj_s.task_status(task_id)
    tasks = proj_s.project_tasks(project_id)
    return render_template('task_list.jinja2', proj_tasks = tasks)

@app.route('/logout')
def logout():
    g.user = None # clear user
    session['user_id'] = None # clear session user id
    return redirect(url_for('login_page')) #return login page

if __name__ == '__main__':
    app.run(debug=True)