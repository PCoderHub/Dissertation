import { Button, Card, Dialog, DialogContent, TextField } from "@mui/material";
import React, { useState } from "react";
import './Register.css';
import axios from "../axiosConfig";
import { useDispatch } from "react-redux";
import { addUserInfo } from "../redux/userSlicer";
import { useNavigate } from "react-router-dom";
import CardPay from "./CardPay";
import { CardElement, useElements, useStripe } from "@stripe/react-stripe-js";

const Register = () => {

    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const stripe = useStripe();
    const elements = useElements();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if(!stripe || !elements) {
            return;
        }

        const result = await stripe.createPaymentMethod({
            type: 'card',
            card: elements.getElement(CardElement),
            billing_details: {
                email: email,
            }
        });

        if (result.error) {
            console.log(result.error.message);
        } else {
            const respo = await axios.post('/subscribe', {
                email: email,
                payment_method: result.paymentMethod.id,
            })
            const {client_secret, status} = respo.data;

            if (status == 'requires_action') {
                stripe.confirmCardPayment(client_secret).then(function(result) {
                    if (result.error) {
                        console.log(result.error.message);
                    } else {
                        console.log('Subscription successful!');
                    }
                })
            } else {
                let memberData = {
                    firstname: firstName,
                    lastname: lastName,
                    email: email,
                    password: password
                }
        
                const response = axios.post('/register', memberData).then((res) => {
                    alert('Subscription successful, Login to continue!!');
                }).catch((err) => alert(err.response.data.message));
                setFirstName('');
                setLastName('');
                setEmail('');
                setPassword('');
            }
        }
    }

    return <Card className="register-container">
        <h1 className="register-title">Register</h1>
        <form className="registerform-container" onSubmit={handleSubmit}>
            <TextField className="register-textfield" label="First Name" variant="standard" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
            <TextField className="register-textfield" label="Last Name" variant="standard" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
            <TextField className="register-textfield" label="Email" variant="standard" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <TextField className="register-textfield" label="Password" variant="standard" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <div className="register-textfield">
            <CardPay />
            </div>
            <Button className="register-button" variant="contained" color="primary" type="submit" >Subscribe</Button>
        </form>
    </Card>
}

export default Register;