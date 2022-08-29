import React, { useState } from "react";

function Registration() {
  const [inputs, setInputs] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Values : ", inputs);
    var data = JSON.stringify(inputs);
    console.log("Data : ", data);
    try {
      fetch("http://127.0.0.1:8000/student/add", {
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
              alert("Student Added succesfully");
              window.location.href = "/";
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

  const handleChange = (e) => {
    e.preventDefault();
    const name = e.target.name;
    const value = e.target.value;
    setInputs((values) => ({ ...values, [name]: value }));
  };

  return (
    <div>
      <h2>Sign Up</h2>
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
          Enter Email :
          <input
            type="text"
            name="email"
            value={inputs.email || ""}
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
    </div>
  );
}

export default Registration;
