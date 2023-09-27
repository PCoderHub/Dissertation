import React, { useEffect, useState } from "react";
import LeftNav from "./LeftNav";
import { Button, Card, FormControl, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import './IssueBooks.css';
import axios from "../axiosConfig";

const IssueBooks = () => {

    const [members, setMembers] = useState();
    const [books, setBooks] = useState();
    const [mem, setMem] = useState('');
    const [bo, setBo] = useState('');
    const [iDate, setIDate] = useState('');
    const [rDate, setRDate] = useState('');

    const getMembers = () => {
        const response = axios.get('/login').then((res) => setMembers(res.data)).catch((err) => console.error(err));
    }

    const getBooks = () => {
        const response = axios.get('/books').then((res) => setBooks(res.data)).catch((err) => console.error(err));
    }

    useEffect(() => {
        getMembers();
        getBooks();
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();

        let issueData = {
            book: bo,
            member: mem,
            idate: iDate,
            rdate: rDate
        }

        const response = axios.post('/issues', issueData).then((res) => {
            console.log(res.data);
            const bookDetail = axios.get(`/books/${res.data.book}`).then((respo) => {
                let bookDetail = {
                    title: respo.data.title,
                    author: respo.data.author,
                    isbn13: respo.data.isbn13,
                    s_loc: respo.data.s_loc,
                    qty: respo.data.qty - 1
                }
                const resp = axios.put(`/books/${res.data.book}`, bookDetail).then((res) => console.log(res)).catch((err) => console.error(err));
            })
        }).catch((err) => alert(err.response.data.message));

        setBo('');
        setMem('');
        setIDate('');
        setRDate('');
    }

    return <div className="issue-book-container">
        <LeftNav/>
        <Card className="issue-book-form">
            <h1 className="issue-book-title">Issue Books</h1>
            <form className="issue-book-form-container" onSubmit={handleSubmit}>
                <FormControl className="issue-book-form-control" sx={{margin: '10px', width: 350}} required >
                    <InputLabel id="book">Book</InputLabel>
                    <Select labelId="book" id="bookname" value={bo} onChange={(e) => setBo(e.target.value)}>
                        <MenuItem value=""><em>None</em></MenuItem>
                        {books?.map((book, i) => {
                            return (
                                <MenuItem key={i} value={book.isbn13}>{book.title}</MenuItem>
                            );
                        })}
                    </Select>
                </FormControl>
                <FormControl className="issue-book-form-control" sx={{margin: '10px', width: 350}} required >
                    <InputLabel id="member">Member</InputLabel>
                    <Select labelId="member" id="membername" value={mem} onChange={(e) => setMem(e.target.value)}>
                        <MenuItem value=""><em>None</em></MenuItem>
                        {members?.map((member, i) => {
                            return(
                                <MenuItem key={i} value={member.email}>{`${member.email}`}</MenuItem>
                            );
                        })}
                    </Select>
                </FormControl>
                <TextField className="issue-book-textfield" label="Issued Date" type="date" sx={{margin: '10px', width: 350}} value={iDate} onChange={(e) => setIDate(e.target.value)} required />
                <TextField className="issue-book-textfield" label="Return Date" type="date" sx={{margin: '10px', width: 350}} value={rDate} onChange={(e) => setRDate(e.target.value)} required />
                <Button className="issue-book-button" variant="contained" color="primary" type="submit" sx={{margin: '10px', width: 350}} >Issue</Button>
            </form>
        </Card>
    </div>
}

export default IssueBooks;