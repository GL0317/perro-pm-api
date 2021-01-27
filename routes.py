from flask import request, jsonify, Response
import data
import db

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

    def post(self, entity, kind):
        entityId = None
        if request.content_type == "application/json":
            newEntity = query.add(entity, kind)
            return newEntity, 201
        return jsonify(ERROR_MSG["415"]), 415

    def get(self, kind):
        return query.retrieve(kind)


class RequestMethods(Routes):
    def __init__(self):
        Routes.__init__(self)

    def get_and_post(self, kind, e_id=None):
        if request.method == 'POST':
            entity = None
            content = request.get_json()
            try:
                if kind == data.PROJECTS:
                    entity = data.Project(content["title"], content["manager"])
                    return super().post(entity.get_project(), kind)
                elif kind == data.USERS:
                    entity = data.User(content)
                    return super().post(entity.get_user(), kind)
                elif kind == data.TASKS:
                    entity = data.Task(content)
                    entity.assign_project(e_id)
                    print(entity) ################################
                return super().post(entity.get_task(), kind)
            except KeyError:
                print("Error: key error when setting data")
                return jsonify(ERROR_MSG["400"]), 400
            except TypeError:
                 print("POST Type Error Exception")
                 return jsonify(ERROR_MSG["400"]), 400
        elif request.method == 'GET':
            return super().get(kind)
