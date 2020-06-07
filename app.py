import bcrypt
from flask import Flask, render_template, request, session, url_for, redirect, g

from utils.manage_users import current_users_list, create_user_func

app = Flask(__name__)
app.secret_key = 'somesecretkey'

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        users_list = current_users_list()
        user = [x for x in users_list if x['user_id'] == session['user_id']][0]
        g.user = user

@app.route('/')
def main_page():
    return redirect(url_for('login_page'))

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        try:
            users_list = current_users_list()
            user = [x for x in users_list if x['username'] == username][0]
            user_password = bytes(user['password'], encoding='utf-8')
            if bcrypt.checkpw(password, user_password):
                session['user_id'] = user['user_id']
                return redirect(url_for('user_dashboard'))
        except:
            pass
    return render_template('login.html')

@app.route('/create_user', methods = ['GET', 'POST'])
def new_user_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        password_re = request.form['password_re'].encode('utf-8')
        if password == password_re:
            users_list = current_users_list()
            users = [x for x in users_list if x['username'] == username]
            for u in users:
                if username == u['username']:
                    return f'{username} already exists.'
            password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
            
            create_user_func(len(users_list),username,password_hash.decode('utf-8'))
            return redirect(url_for('login_page'))
        else:
            return "Passwords don't match."
    return render_template('create_user.html')


@app.route('/user_dashboard')
def user_dashboard():
    if not g.user:
        return redirect(url_for('login_page'))

    return render_template('user_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

