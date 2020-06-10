from datetime import datetime
from database.json_services import json_add_task, json_add_proj


def new_project(project_name, deadline, start_date):

        dline = datetime.strptime(deadline, '%d/%m/%Y')
        stdate = datetime.strptime(start_date, '%d/%m/%Y')

        if stdate < dline:
            return False
        else:
            json_add_proj(project_name, deadline, start_date)
    
def create_task(project_name, task):
    new_task = task
    project_name = project_name
    json_add_task(project_name, new_task)




