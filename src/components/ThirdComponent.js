import React, { createContext, useContext } from "react";
import { UserContext } from "./FirstComponent";
import FourthComponent from "./FourthComponent";

function ThirdComponent() {
  const { user, val } = useContext(UserContext);
  console.log("Third component : ", user);
  return (
    <div>
      <h2>
        ThirdComponent {user.username} {user.age} {val}
      </h2>
      <FourthComponent />
    </div>
  );
}

export default ThirdComponent;
