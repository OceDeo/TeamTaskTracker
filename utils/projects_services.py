from datetime import datetime
import database.json_services as js_srv



def new_project(project_name, deadline, start_date, user_id):
    dline = datetime.strptime(deadline, '%Y-%m-%d')
    stdate = datetime.strptime(start_date, '%Y-%m-%d')
    if stdate > dline:
        return False
    else:
        year, month, day = deadline.split('-')
        deadline = (f'{day}/{month}/{year}')
        year, month, day = start_date.split('-')
        start_date = (f'{day}/{month}/{year}')
        js_srv.json_add_proj(project_name, deadline, start_date, user_id)
    
    
def create_task(project_id, task):
    js_srv.json_add_task(project_id, task)


def check_proj_users(project_name, user_data):
    users = js_srv.current_users_list()
    for user in users:
        if user_data in user['user_id'] or user_data in user['username']:
            js_srv.add_proj_user(project_name, user['user_id'])
    else:
        pass

def specific_proj(project_id):
    projects = js_srv.current_proj_list()
    for project in projects:
        if int(project_id) == project['id']:
            return project


def remove_user(project_id, user_id):
    js_srv.json_remove_user_proj(project_id,user_id)

def edit_proj(project_id, project_name, start_date, deadline):
    js_srv.json_edit_proj(project_id, project_name, start_date, deadline)