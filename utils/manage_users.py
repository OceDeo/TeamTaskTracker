import json

def current_users_list():
    
    users_list = []

    with open('database/user_database.json', 'r') as users:
        user_data = json.load(users)
        user_data = user_data['users']
        for u in user_data:
            users_list.append(u)
    return users_list

def create_user_func(user_id, username, password):
    new_user = {'user_id':(user_id), 'username':(username), 'password':(password)}

    users_list = current_users_list()

    for u in users_list:
        if new_user['username'] == u['username']:
            print('Username Taken')
            break
    else:
        with open ('database/user_database.json', 'r') as add_new_user:
            users = json.load(add_new_user)
            temp = users['users']
            temp.append(new_user)
        with open ('database/user_database.json', 'w') as add_new_user:
            json.dump(users, add_new_user, indent=4)