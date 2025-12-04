import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useCopilotReadable } from '@copilotkit/react-core';
const Logout = ({ setIsAuthenticated }) => {
    const navigate = useNavigate();

    useEffect(() => {
        localStorage.removeItem("accessToken"); // ✅ Remove token
        setIsAuthenticated(false); // ✅ Update state
        navigate("/login"); // ✅ Redirect to login page
    }, [navigate, setIsAuthenticated]);
useCopilotReadable({
  description: "User logout process",
  value: "User is being logged out and redirected to login page"
});
    return <h2>Logging out...</h2>;
};

export default Logout;
