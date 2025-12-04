import React from "react";
import { useCopilotReadable } from '@copilotkit/react-core';


function Create() {
  useCopilotReadable({
  description: "Welcome to Pinterest signup section",
  value: `Password inspiration grid`
});
  return <h1>Welcome to the Create Page</h1>;
}

export default Create;