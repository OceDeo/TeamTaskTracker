import json


def current_users_list():
    users_list = []
    with open('database/user_database.json', 'r') as users:
        user_data = json.load(users)
        user_data = user_data['users']
        for u in user_data:
            users_list.append(u)
    return users_list


def current_proj_list():
    with open('database/projects.json', 'r') as add_new_project:
        projects = json.load(add_new_project)
        return projects['projects']
        

def json_add_proj(project_name, deadline, start_date, user_id):
    proj_id = len(current_proj_list()) 
    new_project = {
        "id": proj_id,
        "project_name": project_name, 
        "users": [user_id], 
        "start_date": start_date, 
        "deadline": deadline, 
        "tasks": []
        }
    with open('database/projects.json', 'r') as add_new_project:
        projects = json.load(add_new_project)
        temp = projects['projects']
        temp.append(new_project)
    with open('database/projects.json', 'w') as add_new_project:
        json.dump(projects, add_new_project, indent=4)


def json_add_task(project_id, new_task):
    with open('database/projects.json', 'r') as add_new_task:
        tasks = json.load(add_new_task)
        temp = tasks['projects']
        for proj in temp:
            if proj['id'] == int(project_id):
                proj['tasks'].append(new_task)
    with open('database/projects.json', 'w') as add_new_task:
        json.dump(tasks, add_new_task, indent=4)


def json_add_user(user_id, username, password):
    new_user = {'user_id':(user_id), 'username':(username), 'password':(password)}
    with open('database/user_database.json', 'r') as add_new_user:
        users = json.load(add_new_user)
        temp = users['users']
        temp.append(new_user)
    with open ('database/user_database.json', 'w') as add_new_user:
        json.dump(users, add_new_user, indent=4)


def add_proj_user(project_name, user_id):
    with open('database/projects.json', 'r') as add_proj_user:
        proj_users = json.load(add_proj_user)
        temp = proj_users['users']
        for proj in temp:
            if proj['project_name'] == project_name:
                proj['users'].append(user_id)
    with open('database/projects.json', 'w') as add_proj_user:
        json.dump(proj_users, add_proj_user, indent=4)

### EDIT PROJECT DETAILS JSON ###

def json_remove_user_proj(project_name, user_id):
    with open ('database/projects.json', 'r') as remove_user:
        users = json.load(remove_user)
        temp = users['projects']
        for proj in temp:
            if user_id in proj['users']:
                proj['users'].remove(user_id)
    with open('database/projects.json', 'w') as remove_user:
        json.dump(users, remove_user, indent=4)

def json_edit_proj(proj_id, project_name, start_date, deadline):
    with open('database/projects.json', 'r') as edit_proj:
        edits = json.load(edit_proj)
        temp = edits['projects']
        for proj in temp:
            if proj_id == proj['id']:
                if project_name != None:
                    proj['project_name'] = project_name
                elif start_date != None:

                    proj['start_date'] = start_date
                elif deadline != None:
                    proj['deadline'] = deadline
                else:
                    pass
    with open('database/projects.json', 'w') as edit_proj:
        json.dump(edits, edit_proj, indent=4)