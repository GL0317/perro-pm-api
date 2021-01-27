import datetime
import json


PROJECTS = 'projects'
USERS = 'users'
TASKS = 'tasks'

def deserialize_date(obj, option=False):
    if option:
        obj = json.dumps(obj)
        obj = json.loads(obj)
    print(obj) ################
    tempList = obj.keys()
    if 'date' in tempList:
        temp = json.dumps(obj, indent=4, default=str)
        temp = json.loads(temp)
        obj = temp.copy()
    return obj


class Project:
    def __init__(self, title, manager):
        self.title = title
        self.manager = manager
        self.date = datetime.datetime.today()

    def get_project(self):
        project = dict(title=self.title, manager=self.manager, date=None)
        ########date_format = datetime.date.strftime(self.date, "%m/%d/%Y")
        # resolve json non-serialized type problem
        ######date_format = json.dumps(date_format, default=json.json_util.default)
        ###### project['date'] = str(date_format)
        ###### project['date'] = date_format
        ###### temp = json.dumps(project, indent=4, default=str)
        ###### temp = json.loads(temp)
        ###### project = temp.copy()
        ###### project = deserialize_date(project)
        return project


class User:
    def __init__(self, user_data):
        self.user = dict(first_name=user_data["first_name"]
                         , last_name=user_data["last_name"]
                         , role=user_data["role"]
                         , project=user_data["project"]
                         , user_name=user_data["user_name"])

    def get_user(self):
        return self.user


class Task:
    def __init__(self, task_data):
        self.task = dict(title=task_data["title"]
                         , description=task_data["description"]
                         , due_date=task_data["due_date"]
                         , assignee=task_data["assignee"])

    def assign_project(self, project_id):
        self.task['project'] = project_id

    def get_task(self):
        return self.task