import React, { useEffect, useState } from "react";
import LeftNav from "./LeftNav";
import './Defaulter.css';
import axios from '../axiosConfig';

const Defaulter = () => {

    const [defaulters, setDefaulters] = useState();

    /*const getIssues = () => {
        const response = axios.get('/issues').then((res) => setIssues(res.data)).catch((err) => console.log(err));
    }

    const memberFine = () => {
        issues?.filter(issue => (issue.status == 'defaulter' || issue.status == 'returned with delay')).map((defaulter, k) => {
            const fine = defaulter.status == 'returned with delay' ? Math.floor(Math.abs(new Date(defaulter.actret).getTime() - new Date(defaulter.rdate).getTime())/(1000*3600*24)) : Math.floor(Math.abs(new Date().getTime() - new Date(defaulter.rdate).getTime())/(1000*3600*24));
        })
    }*/

    const getDefaulters = () => {
        const response = axios.get('/defaulter').then((res) => setDefaulters(res.data)).catch((err) => console.error(err))
    }

    useEffect(() => {
        getDefaulters();
    }, []);

    return <div className="defaulter-container">
        <LeftNav/>
        <div className="defaulter-card">
            <h1 className="defaulter-title">Defaulter List</h1>
            <table className="defaulter-table">
                <thead>
                    <tr>
                        <th className="defaulter-expand">Member</th>
                        <th>Fine</th>
                        <th>Paid/Not Paid</th>
                    </tr>
                </thead>
                <tbody>
                    {defaulters?.map((def, k) => {
                        return (
                            <tr key={k}>
                                <td>{def.member}</td>
                                <td>{def.dues}</td>
                                <td>{def.status}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    </div>
}

export default Defaulter;