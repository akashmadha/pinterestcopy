import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import './SearchBar.css';

const Profile = ({ onUserData }) => {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const token = localStorage.getItem("accessToken");

        if (!token) {
            navigate("/login"); // Redirect to login if no token
            return;
        }

        fetch("https://pinterestclone-backend.onrender.com/api/profile/", {
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
        .then(data => {
  setUser(data);
  if (onUserData) onUserData(data); // ✅ Send data to Navbar
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
                    {user.first_letter}
                </button>
            ) : (
                <p>Loading profile...</p>
            )}
        </div>
    );
};

export default Profile;
