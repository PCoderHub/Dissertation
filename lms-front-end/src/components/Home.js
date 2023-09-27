import React from "react";
import LeftNav from "./LeftNav";
import { useSelector } from "react-redux";
import { Card } from "@mui/material";
import './Home.css';

const Home = () => {

    const userData = useSelector(
        (state) => state.user.user
    );
    return <div className="home-container">
        <LeftNav/>
        {userData.role == 'admin' ? <Card className="home-card">
            <h1 className="home-title">Hi Admin</h1>
            <h2 className="home-heading">Welcome to LMS</h2>
            <ul>
                <li>Provide services to members who have already returned previously issued books.</li>
                <li>Provide services to members who have paid their pending dues.</li>
            </ul>
        </Card> : <Card className="home-card">
            <h1 className="home-title">Hi {userData.email}</h1>
            <h2 className="home-heading">Welcome to XYZ library online app.</h2>
            <p>To continue using our services:</p>
            <ul>
                <li>Return previously borrowed books.</li>
                <li>Check 'Dues' page and pay dues, if any.</li>
                <li>For any questions or queries:
                    <ul>
                        <li>Email: xyz@lms.com</li>
                        <li>Phone: 01234567890</li>
                    </ul>
                </li>
            </ul>
            </Card>}
    </div>
}

export default Home;