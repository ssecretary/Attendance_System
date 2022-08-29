import React, { useState } from "react";

function Login() {
  const [inputs, setInputs] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Values : ", inputs);
    var data = JSON.stringify(inputs);
    console.log("Data : ", data);
    try {
      fetch("http://127.0.0.1:8000/student/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: data,
      }).then((res) => {
        console.log("Res : ", res);
        if (res.ok) {
          res.json().then((val) => {
            if (val.code === 200) {
              console.log("Val : ", val.message.access_token);
              localStorage.setItem("Token", val.message.access_token);
              alert("Student login successful");
              if (inputs.username === "admin") {
                window.location.href = "/student_list";
              } else {
                window.location.href = `/student_detail/${val.data[0].id}`;
              }
              // setLogin(true);
              // setId(val.data[0].id);
            } else {
              alert(val.message);
            }
          });
        }
      });
    } catch (error) {
      console.log("Error : ", error);
    }
  };

  // const routeChange = () => {
  //   let path = `/registration`;
  //   history.push(path);
  // };

  const handleChange = (e) => {
    e.preventDefault();
    const name = e.target.name;
    const value = e.target.value;
    setInputs((values) => ({ ...values, [name]: value }));
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          {" "}
          Enter Username :
          <input
            type="text"
            name="username"
            value={inputs.username || ""}
            onChange={handleChange}
            required={true}
          />
        </label>
        <br></br>
        <label>
          {" "}
          Enter Password :
          <input
            type="password"
            name="password"
            value={inputs.password || ""}
            onChange={handleChange}
            required={true}
          />
        </label>
        <br></br>
        <input type="submit" />
      </form>
      <button onClick={(event) => (window.location.href = "/registration")}>
        Sign Up
      </button>
      {/* {login ? (
        <div>
          {inputs.username === "admin" ? (
            <AllStudentsList />
          ) : (
            <StudentDetails id={id} />
          )}
        </div>
      ) : (
        <div></div>
      )} */}
    </div>
  );
}

export default Login;
