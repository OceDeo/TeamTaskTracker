from datetime import datetime
import database.db_services as dbs

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
        dbs.ProjectRepository.create_project(project_name, user_id, start_date, deadline)
    
    
def create_task(project_id, task):
    if task == '':
        return None
    else:
        return dbs.TaskRepository.add_task(project_id, task)

def add_proj_users(project_name, user_id):
    dbs.ProjectRepository.add_user_to_project(project_name, user_id)

def specific_proj(project_id):
    return dbs.ProjectRepository.fetch_project(project_id)

def remove_user(project_id, user_id):
    dbs.ProjectRepository.remove_user_from_project(project_id,user_id)

def edit_proj(project_id, project_name, start_date, deadline):
    try:
        year, month, day = deadline.split('-')
        deadline = (f'{day}/{month}/{year}')
    except:
        pass
    try:
        year, month, day = start_date.split('-')
        start_date = (f'{day}/{month}/{year}')
    except:
        pass
    dbs.ProjectRepository.edit_project(project_id, project_name, start_date, deadline)

def project_tasks(project_id):
    return dbs.TaskRepository.tasks_project(project_id)

def delete_task(task_id):
    dbs.TaskRepository.delete_task(task_id)

def task_status(task_id):
    dbs.TaskRepository.task_status(task_id)

def finished_unfinished(project_id):
    tasks = dbs.TaskRepository.tasks_project(project_id)
    num_all = 0
    num_done = 0
    for task in tasks:
        num_all += 1
        if task.task_status == True:
            num_done += 1
    return num_done, num_all

def delete_project(project_id):
    dbs.ProjectRepository.delete_project(project_id)    