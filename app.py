import bcrypt
import json

from flask import Flask, render_template, request, session, url_for, redirect, g
from utils.users_services import current_users_list, create_user_func, validate_login, proj_user
from utils.projects_services import new_project, create_task, specific_proj, edit_proj


app = Flask(__name__) 
app.secret_key = 'dYIbV9GL3VtVyGWq2tp7hybbwCL3Aebz6T80WjuY'

@app.before_request
def before_request(): # check for logged user/any open session
    g.user = None
    if 'user_id' in session:
        users_list = current_users_list()
        user = [x for x in users_list if x['user_id'] == session['user_id']][0]
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
        check, user = validate_login(username, password)
        if check == True:
            session['user_id'] = user['user_id'] # set session to user id
            return redirect(url_for('user_dashboard')) #redirect to user dashboard
        else:
            pass #if anything fails refresh page
    return render_template('login.html') 

@app.route('/create_user', methods = ['GET', 'POST'])
def new_user_page():
    if request.method == 'POST': 
        username = request.form['username'] # new username
        password = request.form['password'] #new password
        password_re = request.form['password_re'] #repeat password
        create_user_func(username, password, password_re) # call create user function and add user to database
        return redirect(url_for('login_page')) # redirect to login page
    return render_template('create_user.html')

@app.route('/user_dashboard', methods = ['GET']) #### TO BE EDITED, PROJECTS MOVED TO MY PROJECTS
def user_dashboard():
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page'))
    projects = proj_user(g.user['user_id'])
    return render_template('user_dashboard.jinja2', projects=projects)

@app.route('/user_dashboard/<project_id>', methods = ['GET', 'POST'])
def project_page(project_id):
    project = specific_proj(project_id)
    if request.method == 'POST':
        task = request.form['add_task']
        create_task(project_id,task)
        return redirect(url_for('project_page', project_id = project_id))
    return render_template('project.html', project = project)

@app.route('/myprojects', methods = ['GET'])
def my_projects():
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page'))
    projects = proj_user(g.user['user_id'])
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
            new_project(name, deadline, start_date, g.user['user_id'])
            return redirect(url_for('my_projects'))
    return render_template('add_project.html')    

@app.route('/edit/<project_id>', methods = ['GET', 'POST'])
def edit_project(project_id):
    if not g.user:
        return redirect(url_for('login_page'))
    current_proj = specific_proj(project_id)
    name = current_proj['project_name']
    start_date = current_proj['start_date']
    deadline = current_proj['deadline']
    if request.method == "POST":
        name = request.form['project_name']
        start_date = request.form['start_date']
        deadline = request.form['deadline']
    return render_template('edit_project.html', name = name, start_date = start_date, deadline = deadline)

@app.route('/logout')
def logout():
    g.user = None
    return redirect(url_for(login_page))


if __name__ == '__main__':
    app.run(debug=True)