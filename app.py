import bcrypt
import json

from flask import Flask, render_template, request, session, url_for, redirect, g
from utils.users_services import current_users_list, create_user_func, validate_login
from utils.projects_services import create_task

app = Flask(__name__) 
app.secret_key = 'somesecretkey'

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


@app.route('/user_dashboard', methods = ['GET', 'POST'])
def user_dashboard():
    if not g.user: # if there isnt any session present redirect to login
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        new_task = request.form['add_task']
        project = request.form['ph']
        create_task(project, new_task)
    with open ('database/projects.json', 'r') as add_new_project: # list all projects 
        projects = json.load(add_new_project)
        projects = projects['projects']

    return render_template('user_dashboard.jinja2', projects=projects)

@app.route('/add', methods = ['POST'])
def add_new_task():
    pass

    
if __name__ == '__main__':
    app.run(debug=True)



