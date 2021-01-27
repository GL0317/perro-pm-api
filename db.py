from google.cloud import datastore
import data
import json

DB = datastore.Client()

class Query:
    def __init__(self):
        self.id = ''
        #self.entity = data.Entity()

    def __assignID(self, body, id=-1):
        self.id = str(id)
        if len(self.id) >= 1:
            body["id"] = self.id
            # body["self"] = request.url
            # if owner:
            #     body["self"] += "/" + str(owner)
            # body["self"] += "/" + str(self.id)
            # body["self"] = request.url + "/" + str(self.id)
        return body

    def add(self, data, kind):
        entity = datastore.Entity(key=DB.key(kind))
        entity.update(data)
        DB.put(entity)
        responseBody = json.dumps(entity)
        responseBody = json.loads(responseBody)
        id = entity.id
        # if not id:
        #     id = entity.id
        responseBody = self.__assignID(responseBody, id)
        return responseBody

    def retrieve(self, kind):
        query = DB.query(kind=kind)
        #########results = list(data.deserialize_date(query.fetch()))
        results = list(query.fetch())
        for e in results:
            #########e = data.deserialize_date(e, True)
            # remove passwords for users only
            id = e.key.id
            # if kind == data.USERS:
            #     e = self.entity.removeUserPwd(e)
            #     e.pop('firstName')
            #     e.pop('lastName')
            #     id = e['uniqueId']
            #     e.pop('uniqueId')
            e = self.__assignID(e, id)
        return json.dumps(results)



