import React, { useEffect, useState } from "react";
import LeftNav from "./LeftNav";
import ChatIcon from '@mui/icons-material/Chat';
import axios from "../axiosConfig";
import './ViewMembers.css';
import { Button, Dialog, DialogContent, DialogTitle, TextField } from "@mui/material";

const ViewMembers = () => {

    const [members, setMembers] = useState();

    const getMembers = () => {
        const response = axios.get('/login').then((res) => setMembers(res.data)).catch((err) => console.error(err));
    }

    useEffect(() => {
        getMembers();
    }, []);

    return <div className="view-member-container">
        <LeftNav />
        <div className="view-member-card">
            <h1 className="view-member-title">Library Members</h1>
            <table className="view-member-table">
                <thead>
                    <tr>
                        <th>Sl No</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th className="view-member-expand">Email</th>
                        <th>Chat</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        members?.map((member, i) => {
                            return (
                                <tr key={i}>
                                    <td>{i + 1}</td>
                                    <td>{member.firstname}</td>
                                    <td>{member.lastname}</td>
                                    <td className="email">{member.email}</td>
                                    <td><ChatIcon /></td>
                                </tr>
                            );
                        })
                    }
                </tbody>
            </table>
        </div>
    </div>
}

export default ViewMembers;