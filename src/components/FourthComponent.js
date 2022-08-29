import React, { useContext, useState } from "react";
import FifthComponent from "./FifthComponent";
import { UserContext } from "./FirstComponent";

function FourthComponent() {
  const { callFunction } = useContext(UserContext);
  const [count, setCount] = useState(0);

  const onButtonClick = () => {
    setCount((prevCount) => count + 1);
    callFunction(count);
  };

  return (
    <div>
      <h2>FourthComponent</h2>
      <button onClick={onButtonClick}>Counter</button>
      <FifthComponent />
    </div>
  );
}

export default FourthComponent;
