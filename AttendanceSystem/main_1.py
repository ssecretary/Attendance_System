from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import datetime
import json

    
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["StudentDatabase"]
mycol = mydb["Students"]

class Student(BaseModel):
    username: str
    email: str
    password: str
    days:int = 0
    is_active: bool = True
    
class LoginStudent(BaseModel):
    username:str
    password:str

app = FastAPI()

@app.get("/create-database")
def create_db():
    return {"Database created successfully"}

@app.get("/")
def get_db_list():
    return{"Hello":myclient.list_database_names()}


@app.post("/registration/")
async def create_student(student: Student):
    try:
        cnt = 0
        print("Student : ", student, "Date : ",datetime.datetime.now())
        myquery = {"username":student.username, "email":student.email}
        mydict = { "username": student.username, "email": student.email, 
                  "password":student.password, "days":1, "is_active":True, 
                  "updated_date":datetime.datetime.now()}
        print(mydict)
        mydoc = mycol.find(myquery)
        for x in mydoc:
            cnt+=1
        if cnt > 0:
            return {"Msg":"This student already exists"}
        
        x = mycol.insert_one(mydict)
        print(x.inserted_id)
        return {"Msg":"Student added successfully"}
    except Exception as ex:
        return {"error":str(ex)}
    
@app.get("/get_all_student")
def get_all_student():
    studetn_list = []
    for x in mycol.find({}):
        studetn_list.append(json.dumps(x))
        print(x)
    return {"list":studetn_list}

@app.get("/get_single_student/{name}")
def get_single_student(name:str, q:Union[str, None] = None):
    try:
        print("Query : ", q)
        mydoc = mycol.find_one({"username":name}, {"_id":0})
        created_date = datetime.datetime.strptime(str(mydoc['updated_date']).split(" ")[0], "%Y-%m-%d")
        current_date = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d")

        # difference between dates in timedelta
        delta = current_date - created_date
        print(f'Difference is {delta.days} days')
        if delta.days == 1:
            newvalues = { "$set": {"is_active":True, "updated_date":datetime.datetime.now()} }
            mycol.update_one({"username":name}, newvalues)
            return {"error":"Your Link is Expired"}
        print(mydoc)
        if not mydoc['is_active']:
            return {"Msg":"You had already submitted your attendence"}
        return{"Msg":mydoc}
    except Exception as ex:
        return{"error":str(ex)}

@app.put("/update_student/{name}")
def update_student(name:str):
    try:
        days = 0
        mydoc = mycol.find_one({"username":name})
        print(mydoc)
        days = mydoc['days']
        created_date = datetime.datetime.strptime(str(mydoc['updated_date']).split(" ")[0], "%Y-%m-%d")
        current_date = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d")

        # difference between dates in timedelta
        delta = current_date - created_date
        print(f'Difference is {delta.days} days')
        if delta.days > 1:
            return {"error":"Your Link is Expired"}
        print(mydoc)
        if not mydoc['is_active']:
            return {"Msg":"You had already submitted your attendence"}
        newvalues = { "$set": { "days": days+1, "is_active":False, "updated_date":datetime.datetime.now()} }
        mycol.update_one({"username":name}, newvalues)

        #print "customers" after the update:
        for x in mycol.find():
          print(x)
        return {"Msg":"Student updated successfully"}
    except Exception as ex:
        return {"error":str(ex)}

@app.delete("/delete_student/{name}")
def delete_student(name:str):
    try:
        myquery = { "username": name }
        x = mycol.delete_many(myquery)
        print(x.deleted_count, "documents deleted")
        return{"Msg":"Students deleted"}
    except Exception as ex:
        return {"error":str(ex)}
    
@app.post("/login")
def login_user(student:LoginStudent):
    try:
        mydoc = mycol.find_one({"username":student.username, "password":student.password}, {"_id":0})
        if mydoc:
            return {"Msg":mydoc}
        return {"Msg":"Username or password incorrect"}
    except Exception as ex:
        return{"error":str(ex)}
    