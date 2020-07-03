import database.db_services as dbs    
import bcrypt

def create_user_func(username, password, password_re):
    password = password.encode('utf-8')
    password_re = password_re.encode('utf-8')

    if password == password_re: # check if passwords match
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt()) # hash the password
        dbs.UserRepository.user_exists_check(username)
    else:
        return "Passwords don't match."
    dbs.UserRepository.add_user(username, password_hash.decode('utf-8'))

def validate_login(username, password):
    try:
        user = dbs.Users.query.filter_by(username=username).first()
        print(user)
        user_password = user.password
        user_password = bytes(user_password, encoding='utf-8') #check if password matches
        if bcrypt.checkpw(password, user_password): 
            return True, user
    except:
        pass

def proj_user(user_id):
    return dbs.ProjectRepository.user_projects(user_id)

def user_by_id(session_id):
    return dbs.Users.query.filter_by(id=session_id).first()

def all_users():
    return dbs.UserRepository.user_list()

