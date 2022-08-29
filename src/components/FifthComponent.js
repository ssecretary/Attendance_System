import React, { createContext, useContext } from "react";
import { UserContext } from "./FirstComponent";

function FifthComponent() {
  const user = useContext(UserContext);
  return (
    <div>
      FifthComponent {user.username} {user.age}
    </div>
  );
}

export default FifthComponent;
