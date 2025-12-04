import React from "react";
import { useCopilotReadable } from '@copilotkit/react-core';
import Navbar from "../Navbar-Bucket/Navbar";

function Message() {
   useCopilotReadable({
    description: "Welcome to Pinterest signup section",
    value: `Password inspiration grid`
  });
  <Navbar />
  return <h1>Welcome to the message Page</h1>;
}

export default Message;