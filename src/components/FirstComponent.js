import React, { createContext, useEffect, useState } from "react";
import SecondComponent from "./SecondComponent";

export const UserContext = createContext();

function FirstComponent(props) {
  const [inputs, setInputs] = useState({});
  const [submitClick, setSubmitClick] = useState(false);
  const [count, setCount] = useState(0);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Values : ", inputs);

    alert(`My name is ${inputs.username} and I am ${inputs.age} years old`);
    setSubmitClick(true);
  };

  const handleChange = (e) => {
    e.preventDefault();
    const name = e.target.name;
    const value = e.target.value;
    setInputs((values) => ({ ...values, [name]: value }));
    console.log("Chnage : ", inputs);
  };

  const propsFromChildren = (val) => {
    console.log("Props from childern : ", val);
  };

  return (
    <UserContext.Provider
      value={{
        user: inputs,
        val: "2nd paramaeter",
        callFunction: (item) => propsFromChildren(item),
      }}
    >
      <div>
        Count : {count}
        <form onSubmit={handleSubmit}>
          <label>
            {" "}
            My name is :
            <input
              type="text"
              name="username"
              value={inputs.username || ""}
              onChange={handleChange}
            />
          </label>
          <br></br>
          <label>
            {" "}
            Enter your age :
            <input
              type="number"
              name="age"
              value={inputs.age || ""}
              onChange={handleChange}
            />
          </label>
          <br></br>
          <input type="submit" />
        </form>
        {submitClick && <SecondComponent />}
      </div>
    </UserContext.Provider>
  );
}

export default FirstComponent;
