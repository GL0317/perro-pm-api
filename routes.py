from flask import request, jsonify, Response
import data
import db
import json

query = db.Query()

ERROR_MSG = {
    "400": {"Bad Request": "The request object is missing at least one of the required attributes or has an" +
                           " incorrect attribute"},
    "401": {"Unauthorized": "Unauthorized request"},
    "403": {"Forbidden": "Request payload is not unique"},
    "404": {"Not Found": "The entity id does not exist"},
    "415": {"Unsupported Media Type": "The request content-type must be json(Content-type = 'application/json'"}
}


class Routes:
    def __init__(self):
        self.id = 0

    def post(self, entity, kind, e_id=None):
        if request.content_type == "application/json":
            newEntity = query.add(entity, kind, e_id)
            return newEntity, 201
        return jsonify(ERROR_MSG["415"]), 415

    def post_user_project(self, entity, kind, e_id):
        # add the project with the user id as the manager
        db_project = query.add(entity, data.PROJECTS)
        # update the user's project list
        db_user = query.retrieve_one(kind, e_id)
        if db_user['project']:
            updated_list = db_user['project'].copy()
        else:
            updated_list = list()
        updated_list.append(db_project['id'])
        user_key = db.DB.key(kind, int(e_id))
        a_user = db.DB.get(user_key)
        a_user['project'] = updated_list
        db.DB.put(a_user)
        return db_project, 201

    def get(self, kind, e_id=None, isProject=False):
        return query.retrieve(kind, e_id, isProject)


class RequestMethods(Routes):
    def __init__(self):
        Routes.__init__(self)

    def get_and_post(self, kind, e_id=None, isProject=False):
        if request.method == 'POST':
            entity = None
            content = request.get_json()
            try:
                if kind == data.PROJECTS or isProject is True:
                    entity = data.Project(content)
                    # handle project creation for the user
                    if kind == data.USERS:
                        entity.add_manager(e_id)
                        return super().post_user_project(entity.get_project(), kind, e_id)
                    return super().post(entity.get_project(), kind)
                elif kind == data.USERS:
                    entity = data.User(content)
                    return super().post(entity.get_user(), kind)
                elif kind == data.TASKS:
                    entity = data.Task(content)
                    entity.assign_project(e_id)
                return super().post(entity.get_task(), kind)
            except KeyError:
                print("Error: key error when setting data")
                return jsonify(ERROR_MSG["400"]), 400
            except TypeError:
                print("POST Type Error Exception")
                return jsonify(ERROR_MSG["400"]), 400
        elif request.method == 'GET':
            # retrieve user assigned projects
            if kind == data.USERS and isProject is True:
                return super().get(data.PROJECTS, e_id, isProject)
            if e_id:
                return super().get(kind, e_id)
            return super().get(kind)
