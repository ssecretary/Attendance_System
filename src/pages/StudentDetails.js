import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function StudentDetails(props) {
  const [studentDetail, setStudentDetail] = useState({});
  const params = useParams();
  console.log("Oarams : ", params.id);
  const bearerToken = localStorage.getItem("Token");

  // const id = props.location.pathname;
  // console.log("Id : ", this.props.location.pathname);
  useEffect(() => {
    try {
      fetch("http://127.0.0.1:8000/student/get_student/" + params.id, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + bearerToken,
        },
      }).then((res) => {
        console.log("Res : ", res.ok);
        if (res.ok) {
          return res.json().then((val) => {
            setStudentDetail(val.data[0]);
          });
        } else {
          if (res.status === 403 || res.status === 401) {
            res.json().then((val) => {
              console.log(val);
              alert(val.detail);
            });
          } else {
            res.json().then((val) => {
              console.log(val);
              alert(val.detail);
            });
          }
        }
      });
    } catch (error) {
      console.log("Error : ", error);
    }
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    // console.log(studentDetail["days"]);
    studentDetail["days"] = studentDetail["days"] + 1;
    var data = JSON.stringify(studentDetail);
    console.log("Data : ", data);
    try {
      fetch("http://127.0.0.1:8000/student/update_student/" + params.id, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + bearerToken,
        },
        body: data,
      }).then((res) => {
        console.log("Res : ", res.ok);
        if (res.ok) {
          res.json().then((val) => {
            console.log("update : ", val);
            if (val.code === 200) {
              alert("Attendance submitted successfully");
              window.location.href = "/";
            } else {
              if (res.status === 403 || res.status === 401) {
                res.json().then((val) => {
                  console.log(val);
                  alert(val.detail);
                });
              } else {
                res.json().then((val) => {
                  console.log(val);
                  alert(val.detail);
                });
              }
            }
          });
        }
      });
    } catch (error) {
      console.log("Error : ", error);
    }
  };
  return (
    <div>
      <h2>StudentDetails</h2>

      {studentDetail && (
        <form onSubmit={handleSubmit}>
          <label>
            {" "}
            Username :
            <input
              type="text"
              name="username"
              value={studentDetail.username || ""}
              disabled={true}
            />
          </label>
          <br></br>
          <label>
            {" "}
            Email :
            <input
              type="text"
              name="email"
              value={studentDetail.email || ""}
              disabled={true}
            />
          </label>
          <br></br>
          <label>
            {" "}
            Attendance Day :
            <input
              type="number"
              name="days"
              value={studentDetail.days || ""}
              disabled={true}
            />
          </label>
          <br></br>
          <input type="submit" value="Submit Attendance" />
        </form>
      )}
    </div>
  );
}

export default StudentDetails;
