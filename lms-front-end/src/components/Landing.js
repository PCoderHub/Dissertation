import React, { useState } from "react";
import {Button, Card} from '@mui/material';
import './Landing.css';
import Register from "./Register";
import Login from "./Login";
import { Elements } from "@stripe/react-stripe-js";

const Landing = ({stripePromise}) => {

    const [toggle, setToggle] = useState('register');

    const handleLogin = () => {
        setToggle('login');
    }

    const handleRegister = () => {
        setToggle('register');
    }

    return <Card className="landing-container">
        <div className="landing-top">
            <h1 className="title">LibrEase</h1><br/><h1 className="subtitle">Become a member and find your favorite books from XYZ library. Subscribe with card details (£5 /month). </h1>
        </div>
        {toggle === 'register' ? <>
        <div>
            <Elements stripe={stripePromise}>
            <Register />
            </Elements>
        </div>
        <div className="bottom-button">
        <Button variant="contained" color="secondary" onClick={handleLogin}>Login</Button>
        </div>
        </> : <>
        <div>
            <Login />
        </div>
        <div className="bottom-button">
        <Button variant="contained" color="secondary" onClick={handleRegister}>Become Member</Button>
        </div>
        </>}
        
    </Card>
}

export default Landing;