    import { useEffect, useState } from "react";
    import { useNavigate, useLocation } from "react-router-dom";
    import "./SearchBar.css";
    import API_BASE_URL from "../../config";
    import { useCopilotReadable } from '@copilotkit/react-core';

    const Profile = ({ onUserData }) => {
        const [user, setUser] = useState(null);
        const navigate = useNavigate();
        const location = useLocation();

        useCopilotReadable({
    description: "Current user profile information",
    value: user 
        ? `User: ${user.username || 'No username'}, Email: ${user.email || 'No email'}, Initial: ${user.initial}`
        : "No user logged in or loading..."
});

        useEffect(() => {
            const token = localStorage.getItem("accessToken");

            if (!token) {
                navigate("/login"); // Redirect to login if no token
                return;
            }

        fetch(`${API_BASE_URL}/api/profile/`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            })
            .then(response => {
                if (response.status === 401) {
                    localStorage.removeItem("accessToken"); 
                    navigate("/login"); 
                }
                return response.json();
            })
            .then((data) => {
            const username = data?.username || "";
            const email = data?.email || "";
            const initial =
                (username || email).charAt(0).toUpperCase() || "U";
            const formatted = {
                ...data,
                username,
                email,
                initial,
                displayName: username || email?.split("@")[0] || "User",
            };
            setUser(formatted);
            if (onUserData) onUserData(formatted);
            })

            .catch(error => console.error("Error fetching profile:", error));
        }, [navigate]);

        const handleProfileClick = () => {
            if (user) {
                navigate("/Profile", { state: { user } }); // ✅ Navigate with user data
            }
        };

        // Show user details if on the `/profile` page
        if (location.pathname === "/Profile") {
            const userDetails = location.state?.user;
            if (!userDetails) {
                navigate("/"); // Redirect back if no user data
                return null;
            }

            return (
                <div>
                    <h2>User Profile</h2>
                    <p><strong>Username:</strong> {userDetails.username}</p>
                    <p><strong>Email:</strong> {userDetails.email}</p>
                </div>
            );
        }

        return (
            <div>
                {user ? (
                    <button className="user_profile" onClick={handleProfileClick}>
                        {user.initial}
                    </button>
                ) : (
                    <p>Loading profile...</p>
                )}
            </div>
        );
    };

    export default Profile;
