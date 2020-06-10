from database.json_services import json_add_user, current_users_list
import bcrypt

def create_user_func(username, password, password_re):
    users_list = current_users_list()
    password = password.encode('utf-8')
    password_re = password_re.encode('utf-8')

    if password == password_re: # check if passwords match
        users_list = current_users_list() #list of all users
        users = [x for x in users_list if x['username'] == username] 
        for u in users: # check if username arleady exists in database
            if username == u['username']:
                return f'{username} already exists.'
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt()) # hash the password
    else:
        return "Passwords don't match."
    json_add_user(len(users_list), username, password_hash.decode('utf-8'))

def validate_login(username, password):
    try:
        users_list = current_users_list() # import list of all users
        user = [x for x in users_list if x['username'] == username][0] #check if username exists
        user_password = bytes(user['password'], encoding='utf-8') #check if password matches
        if bcrypt.checkpw(password, user_password): 
            return True, user
    except:
        pass
