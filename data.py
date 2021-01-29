import datetime
import json


PROJECTS = 'projects'
USERS = 'users'
TASKS = 'tasks'

def deserialize_date(obj, option=False):
    if option:
        obj = json.dumps(obj)
        obj = json.loads(obj)
    temp_list = obj.keys()
    if 'date' in temp_list:
        temp = json.dumps(obj, indent=4, default=str)
        temp = json.loads(temp)
        obj = temp.copy()
    return obj


class Project:
    def __init__(self, project_data):
        self.project = dict(title=project_data['title']
                            , start_date=project_data['start_date']
                            , due_date=project_data['due_date']
                            , description=project_data['description'])

    def get_project(self):
        return self.project

    def add_manager(self, userid):
        self.project['manager'] = userid



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
