import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("Student_Collection")


# helper used to parsed database query into python dict

def student_helper(student) -> dict:
    return {
        "id": str(student['_id']),
        "username": student['username'],
        "email": student["email"],
        "password": student["password"],
        "days": student["days"],
        "is_active": student["is_active"],
        "created_date": student["created_date"]
    }


# Retrieve all student from database
async def get_all_students():
    students = []
    try:
        async for student in student_collection.find():
            students.append(student_helper(student))
        return students
    except Exception as ex:
        raise ex


# Retrieve student with specific id
async def get_specific_student(id: str):
    try:
        student = await student_collection.find_one({"_id": ObjectId(id)})
        if student:
            return student_helper(student)
        return "No such student found"
    except Exception as ex:
        raise ex

async def verify_student(id: str):
    try:
        student = await student_collection.find_one({"_id": ObjectId(id)})

        data = {"is_active":True}

        if student:
            updated_student = await student_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_student:
                return True
            return False
        return "No student with such id"
    except Exception as ex:
        raise ex


# Add new Student
async def add_student(student_data: dict) -> dict:
    try:
        # student = await student_collection.find_one({"email": student_data['email']})
        # if student:
        #     return {"Msg": "Student with this username and email already exists"}
        new_student = await student_collection.insert_one(student_data)
        inserted_student = await student_collection.find_one({"_id": new_student.inserted_id})
        return student_helper(inserted_student)
    except Exception as ex:
        print(ex)
        raise ex


# Update days of student
async def update_student_days(id: str, data: dict):
    try:
        student = await student_collection.find_one({"_id": ObjectId(id)})
        if len(data) < 1:
            return False

        if student:
            updated_student = await student_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_student:
                return True
            return False
        return "No student with such id"
    except Exception as ex:
        raise ex


# Delete Student
async def delete_student(id: str):
    try:
        student = await student_collection.find_one({"_id": ObjectId(id)})
        if student:
            await student_collection.delete_one({"_id": ObjectId(id)})
            return True
        return False
    except Exception as ex:
        raise ex


# Login Student
async def login_student(data: dict):
    try:
        student = await student_collection.find_one({"username": data["username"], "password": data["password"]})
        if student:
            return student_helper(student)
        return False
    except Exception as ex:
        raise ex
