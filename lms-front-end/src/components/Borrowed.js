import React, { useEffect, useState } from "react";
import LeftNav from "./LeftNav";
import { useSelector } from "react-redux";
import axios from "../axiosConfig";
import './Borrowed.css';

const Borrowed = () => {

    const [issues, setIssues] = useState();
    const [books, setBooks] = useState();

    const userData = useSelector(
        (state) => state.user.user
    );

    const getIssues = () => {
        const response = axios.get('/issues').then((res) => {
            setIssues(res.data);
            res.data?.filter(issue => issue.member == userData.email)?.forEach(item => {
                if (item.actret == '' && new Date(item.rdate) < new Date()) {
                    getNotification('')
                } else if (item.actret == '' && new Date(item.rdate) > new Date()) {
                    getNotification(item.rdate);
                }
            });
        }).catch((err) => console.log(err));
    }

    const getBooks = () => {
        const response = axios.get('/books').then((res) => setBooks(res.data)).catch((err) => console.error(err));
    }

    let bookDetails = {};
    books?.map((bo) => {
        bookDetails[bo.isbn13] = bo.title;
    })

    const getTitle = (isb) => {
        const title = Object.keys(bookDetails).filter((is) => is == isb);
        return bookDetails[title[0]];
    }

    const getNotification = (date) => {
        if (date == '') {
            alert('Return your book as soon as possible');
        } else {
            alert(`Remember to return your book by ${new Date(date).toDateString()}`);
        }
    }

    useEffect(() => {
        getIssues();
        getBooks();
    }, []);

    return <div className="borrowed-container">
        <LeftNav/>
        <div className="borrowed-card">
            <h1 className="borrowed-title">Borrowed Books</h1>
            {issues?.filter(issue => issue.member == userData.email)?.length == 0 ? "No history of borrows" : <table className="borrowed-table">
                <thead>
                    <tr>
                        <th className="borrowed-expand">Book</th>
                        <th>Issue Date</th>
                        <th>Return Date</th>
                        <th>Actual Return</th>
                    </tr>
                </thead>
                <tbody>
                    {issues?.filter(issue => issue.member == userData.email)?.map((borrow) => {
                        return (
                            <tr>
                            <td>{getTitle(borrow.book)}</td>
                            <td>{borrow.idate}</td>
                            <td>{borrow.rdate}</td>
                            <td>{borrow.actret}</td>
                        </tr>
                        );
                    })}
                </tbody>
            </table>}
        </div>
    </div>
}

export default Borrowed;