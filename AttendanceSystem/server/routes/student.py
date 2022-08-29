import datetime
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from AttendanceSystem.server.auth.auth_bearer import JWTBearer
from AttendanceSystem.server.auth.auth_handler import signJWT
from AttendanceSystem.server.database import add_student, get_all_students, get_specific_student, update_student_days, \
    delete_student, login_student, verify_student
from AttendanceSystem.server.models.student import Student, ResponseModel, ErrorResponseModel, UpdateStudentModel

router = APIRouter()

PORT = 587
smtp_server = "smtp.gmail.com"
sender_mail = "testingapplication62@gmail.com"
sender_password = "ctynastdyvyjlqbl"
receiver_mail = "testingapplication62@gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "Verification Link"
message["From"] = sender_mail
message["To"] = receiver_mail

@router.post("/login")
async def login_student_call(req: UpdateStudentModel = Body(...)):
    try:
        req = {k: v for k, v in req.dict().items() if v is not None}
        student = await login_student(req)
        if student:
            token = signJWT(student['id'])
            return ResponseModel(student, token)
        return ErrorResponseModel(student, 401, "Invalid Username or Password")
    except Exception as ex:
        return ErrorResponseModel(str(ex), 401, "Error while login")

@router.post("/add", response_description="Student data added")
async def add_student_data(student: Student = Body(...)):
    try:
        student = jsonable_encoder(student)
        new_student = await add_student(student)
        if "Msg" in new_student:
            return ErrorResponseModel(new_student, 400, "Already exists")
        # message = """\
        # Subject : Attendance link
        #
        # link : "http://localhost:3000/student_detail/{}".format(new_student.id)
        # """
        html = """
        <html>
        <head></head>
          <body>
          <h3>Please find  the below link for verifying your account</h3>
            <p>Link:</p>
            <a href="http://localhost:3000/verify_student/$(id)>Verification Link</a>
          </body>
        </html>
        """

        html = html.replace("$(id)", new_student['id'])

        part1 = MIMEText(html, 'html')
        # part2 = MIMEText("Link:\nhttp://www.somewhere.com/whatever.foo", 'text')

        message.attach(part1)
        # msg.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port=PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_mail, sender_password)
            server.sendmail(sender_mail, receiver_mail, message.as_string())
        access_token = signJWT(new_student['id'])
        return ResponseModel(access_token, "Student added Successfully")
    except Exception as ex:
        return ErrorResponseModel(str(ex), 400, "Error while adding data")


@router.get('/get_all', response_description="All students data")
async def get_all_student():
    try:
        students = await get_all_students()
        if students:
            return ResponseModel(students, "Students data retrieved successfully")
        return ResponseModel(students, "Empty list returned")
    except Exception as ex:
        print(ex)
        return ErrorResponseModel(str(ex), 400, "Error while fetching all student")


@router.get("/get_student/{id}", dependencies=[Depends(JWTBearer())])
async def get_student_from_id(id):
    try:
        student = await get_specific_student(id)
        if student and student != "No such student found":
            return ResponseModel(student, "Student retrieved successfully")
        return ResponseModel(student, "No such Student")
    except Exception as ex:
        print(ex)
        return ErrorResponseModel(str(ex), 400, "Error while fetching data")

@router.get("/get_student_for_verification/{id}")
async def get_student_from_id(id):
    try:
        student = await get_specific_student(id)
        if student and student != "No such student found":
            return ResponseModel(student, "Student retrieved successfully")
        return ResponseModel(student, "No such Student")
    except Exception as ex:
        print(ex)
        return ErrorResponseModel(str(ex), 400, "Error while fetching data")

@router.put("/verify_student/{id}")
async def verify_student_from_id(id):
    try:
        student = await verify_student(id)
        if student and student != "No such student found":
            return ResponseModel(student, "Student verified successfully")
        return ResponseModel(student, "No such Student")
    except Exception as ex:
        print(ex)
        return ErrorResponseModel(str(ex), 400, "Error while fetching data")


@router.put("/update_student/{id}", dependencies=[Depends(JWTBearer())])
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    try:
        req = {k: v for k, v in req.dict().items() if v is not None}
        created_date = datetime.datetime.strptime(str(req['created_date']).split(" ")[0], "%Y-%m-%d")
        current_date = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d")

        # difference between dates in timedelta
        delta = current_date - created_date
        print(f'Difference is {delta.days} days')
        if delta.days < 1:
            return ErrorResponseModel("Attendance already submitted", 400, "Already Submitted")
        req['created_date'] = datetime.datetime.now()
        updated_student = await update_student_days(id, req)
        if updated_student:
            return ResponseModel(
                "Student with ID: {} name update is successful".format(id),
                "Attendance done successfully",
            )
        return ErrorResponseModel(
            "An error occurred",
            400,
            "There was an error updating the student data.",
        )
    except Exception as ex:
        return ErrorResponseModel(str(ex), 400, "Error updating data")


@router.delete("/delete_student/{id}")
async def delete_student_data(id):
    try:
        student = await delete_student(id)
        if student:
            return ResponseModel("Student Data deleted successfully", "Data deleted")
        return ErrorResponseModel("Error deleting data", 400,"Error deleting data")
    except Exception as ex:
        print(ex)
        return ErrorResponseModel(str(ex), 400, "Error deleting data")



