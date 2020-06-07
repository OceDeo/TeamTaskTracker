
class Project():

    def __init__(self, project_name, start_date, deadline, team_members_id):
        self.project_name = project_name
        self.start_date = start_date
        self.deadline = deadline
        self.team_members_id = []

    def phases(self, phase):
        current_phase = phase
        return current_phase
    
    def tasks(self, task):
        
        pass

project_1 = Project('Proj1', '01/02/2020', '05/02/2020',[1,2])

print(project_1.phases(1))