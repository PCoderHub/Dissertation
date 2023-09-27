import React, { useEffect, useState } from "react";
import LeftNav from "./LeftNav";
import { useSelector } from "react-redux";
import { Button, Card } from "@mui/material";
import axios from "../axiosConfig";
import CardPay from "./CardPay";
import { CardElement, useElements, useStripe } from "@stripe/react-stripe-js";
import './FinePayment.css';
import { useNavigate } from "react-router-dom";

const FinePayment = () => {

    const [defaulter, setDefaulter] = useState();
    const [issues, setIssues] = useState();
    const [isOngoing, setIsOngoing] = useState(false);
    
    const stripe = useStripe();
    const elements = useElements();
    const navigate = useNavigate();

    const userData = useSelector(
        (state) => state?.user?.user
    );

    const getDefaulter = () => {
        const response = axios.get('/defaulter').then((res) => setDefaulter(res.data)).catch((err) => console.log(err));
    }

    const getIssues = () => {
        const response = axios.get('/issues').then((res) => setIssues(res.data)).catch((err) => console.error(err));
    }

    useEffect(() => {
        getDefaulter();
        getIssues();
    }, []);

    const handleSubmit = async (item) => {

        if (!stripe || !elements) {
            return;
        }
        
        setIsOngoing(true);

        const response = await axios.post('/fine', {
            email: item.member,
            fine: Math.round(item.dues*100)
        });
        const clientSecret = response.data['secret'];

        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: elements.getElement(CardElement),
                billing_details: {
                    email: userData.email
                },
            },
        });

        console.log(result);

        if (result.error) {
            console.log(result.error.message);
        } else {
            if (result.paymentIntent.status == 'succeeded') {
                const resp = axios.put(`/defaulter/${item.id}`, {
                    member: userData.email,
                    dues: item.dues,
                    status: 'paid'
                }).then((res) => console.log(res)).catch((err) => console.error(err));
                issues.filter((issue) => (issue.member == userData.email && (issue.status == 'returned with delay' || issue.status == 'defaulter'))).forEach((item) => {
                    if (item.actret == '') {
                        const respo = axios.put(`/issues/${item.id}`, {
                            book: item.book,
                            member: item.member,
                            idate: item.idate,
                            rdate: new Date().toISOString().substring(0, 10),
                            actret: item.actret,
                            status: 'dues paid, not returned'
                        }).then((res) => console.log(res)).catch((err) => console.error(err));
                    } else {
                        const respo = axios.put(`/issues/${item.id}`, {
                            book: item.book,
                            member: item.member,
                            idate: item.idate,
                            rdate: item.rdate,
                            actret: item.actret,
                            status: 'returned with delay, dues paid'
                        }).then((res) => console.log(res)).catch((err) => console.error(err));
                    }
                })
                setIsOngoing(false);
                alert('Payment Successful!')
            }
        }
    }

    return <div className="fine-container">
        <LeftNav/>
        <Card className="fine-card">
            {defaulter?.filter((defaulter) => (defaulter.member == userData.email && defaulter.status == 'unpaid')).length == 0 ? <h2 className="fine-title">Total dues: £0</h2> : defaulter?.filter((defaulter) => (defaulter.member == userData.email && defaulter.status == 'unpaid')).map((item, k) => {
                return (
                    <div className="fine-card-container">
                    <h2 className="fine-title">Total dues: £{item.dues}</h2>
                    <CardPay className="fine-card-element" />
                    <Button className="fine-button" onClick={() => handleSubmit(item)} disabled={isOngoing || !stripe || !elements}>{isOngoing ? 'Processing...' : 'Pay'}</Button>
                    </div>
                );
            })}
        </Card>
    </div>
}

export default FinePayment;