from google.cloud import datastore
import data
import json

DB = datastore.Client()

class Query:
    def __init__(self):
        self.id = None

    def __assignID(self, body, id=-1):
        self.id = str(id)
        if len(self.id) >= 1:
            body["id"] = self.id
        return body

    def add(self, data, kind):
        entity = datastore.Entity(key=DB.key(kind))
        entity.update(data)
        DB.put(entity)
        response_body = json.dumps(entity)
        response_body = json.loads(response_body)
        id = entity.id
        response_body = self.__assignID(response_body, id)
        return response_body

    def retrieve(self, kind, e_id=None, is_project=False):
        query = DB.query(kind=kind)
        if kind == data.TASKS and e_id != None:
            # get tasks for a specific project
            query.add_filter("project", "=", e_id)
        elif is_project is True and e_id != None:
            query.add_filter("manager", "=", e_id)
        results = list(query.fetch())
        for e in results:
            # remove passwords for users only
            id = e.key.id
            e = self.__assignID(e, id)
        return json.dumps(results)

    def retrieve_one(self, kind, e_id):
        key = DB.key(kind, int(e_id))
        entity = DB.get(key)
        return entity




