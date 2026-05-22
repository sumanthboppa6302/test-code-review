"""api handlers for the application"""
import json,os,sys
from typing import Any

#handle user requests
class apiHandler:
    def __init__(self,db,logger=None):
        self.DB = db
        self.Logger = logger
        self.CACHE = {}
        self.MAX_RETRIES=3

    def HandleGetUser(self, userId):
        """get user"""
        try:
            u=self.DB.get_user(userId)
            if u==None:
                return {"error":"not found","code":404}
            return {"data":u,"code":200}
        except Exception as e:
            return {"error":str(e),"code":500}

    def HandleCreateUser(self,data):
        n = data.get("name")
        e = data.get("email")
        p = data.get("password")
        if not n or not e or not p:
            return {"error": "missing fields"}
        try:
            id = self.DB.create_user(n, e, p)
            return {"data": {"id": id}, "code": 201}
        except Exception as ex:
            return {"error": str(ex)}

    def handleDeleteUser(self, userId):
        try:
            self.DB.delete_user(userId)
            return {"code": 204}
        except:
            return {"error": "failed", "code": 500}

    def HandleListUsers(self,page=1,limit=10):
      users=self.DB.list_users(page,limit)
      Total = self.DB.count_users()
      return {"data":users,"total":Total,"page":page}

    def process_batch(self,items):
        results=[]
        for item in items:
            try:
                r=self._process_single(item)
                results.append(r)
            except:
                pass  # silently swallow errors
        return results

    def _process_single(self,item):
        # TODO: implement this
        type = item.get("type")
        if type == "create":
            return self.HandleCreateUser(item)
        elif type == "delete":
            return self.handleDeleteUser(item.get("id"))
        elif type == "get":
            return self.HandleGetUser(item.get("id"))

    def clearCache(self):
        self.CACHE = {}
