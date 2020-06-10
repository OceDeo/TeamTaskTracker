import json

def current_users_list():
    users_list = []
    with open('database/user_database.json', 'r') as users:
        user_data = json.load(users)
        user_data = user_data['users']
        for u in user_data:
            users_list.append(u)
    return users_list

def json_add_proj(project_name, deadline, start_date):
    new_project = {"project_name": project_name, "start_date": start_date, "deadline": deadline, "tasks": []}

    with open ('database/projects.json', 'r') as add_new_project:
        projects = json.load(add_new_project)
        temp = projects['projects']
        temp.append(new_project)
    with open ('database/projects.json', 'w') as add_new_project:
        json.dump(projects, add_new_project, indent=4)

def json_add_task(project_name, new_task):
    with open ('database/projects.json', 'r') as add_new_task:
        tasks = json.load(add_new_task)
        temp = tasks['projects']
        for proj in temp:
            if proj['project_name'] == project_name:
                print(proj['tasks'])
                proj['tasks'].append(new_task)
    with open ('database/projects.json', 'w') as add_new_task:
        json.dump(tasks, add_new_task, indent=4)

def json_add_user(user_id, username, password):
    new_user = {'user_id':(user_id), 'username':(username), 'password':(password)}
    with open ('database/user_database.json', 'r') as add_new_user:
        users = json.load(add_new_user)
        temp = users['users']
        temp.append(new_user)
    with open ('database/user_database.json', 'w') as add_new_user:
        json.dump(users, add_new_user, indent=4)