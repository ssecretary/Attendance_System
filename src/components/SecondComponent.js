import React, { useEffect, useRef, useState } from "react";
import ThirdComponent from "./ThirdComponent";

function SecondComponent() {
  const [input, setInput] = useState("");

  return (
    <div>
      <h2>SecondComponent</h2>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <ThirdComponent />
    </div>
  );
}

export default SecondComponent;
