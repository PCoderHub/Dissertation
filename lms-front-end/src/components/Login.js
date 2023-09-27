import { Button, Card, Dialog, DialogContent, DialogTitle, TextField } from "@mui/material";
import React, { useState } from "react";
import './Login.css';
import axios from "../axiosConfig";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { addUserInfo } from "../redux/userSlicer";

const Login = () => {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [open, setOpen] = useState(false);
    const [resetP, setResetP] = useState('');

    const navigate = useNavigate();
    const dispatch = useDispatch();

    const handleSubmit = (e) => {
        e.preventDefault();

        let loginData = {
            email: email,
            password: password
        }

        const response = axios.post('/login', loginData).then((res) => {
            dispatch(addUserInfo({
                email: res.data.email,
                role: res.data.role
            }));
            navigate('/home');
        }).catch((err) => alert(err.response.data.message));
    }

    const handleClickOpen = (issue) => {
        setOpen(true);
    }

    const handleClickClose = () => {
        setOpen(false);
    }

    const handleReset = (e) => {
        e.preventDefault();
        let editedUser = {
            email: email,
            newpassword: resetP
        }
        const response = axios.put('/resetpassword', editedUser).then((res) => alert(res.data.message)).catch((err) => console.error(err));
        handleClickClose();
    }

    return <Card className="login-container">
        <h1 className="login-title">Login</h1>
        <form className="loginform-container" onSubmit={handleSubmit}>
            <TextField className="login-textfield" label="Email" variant="standard" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <TextField className="login-textfield" label="Password" variant="standard" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <Button className="login-button" variant="contained" color="primary" type="submit" >Login</Button>
            <Button onClick={handleClickOpen}>Forgot Password?</Button>
            <Dialog fullWidth open={open} onClose={handleClickClose}>
                <DialogTitle className='return-edit-title'>Reset Password</DialogTitle>
                <DialogContent>
                    <form className="loginform-container" onSubmit={handleReset}>
                        <TextField className="login-textfield" label="New password" variant="standard" type="password" value={resetP} onChange={(e) => setResetP(e.target.value)}/>
                        <Button className="login-button" type="submit">Reset</Button>
                    </form>            
                </DialogContent>
            </Dialog>
        </form>
    </Card>
}

export default Login;