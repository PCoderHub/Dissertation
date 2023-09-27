import React, { useState } from "react";
import './AddBook.css';
import LeftNav from "./LeftNav";
import { Button, Card, TextField } from "@mui/material";
import axios from "../axiosConfig";

const AddBook = () => {

    const [title, setTitle] = useState('');
    const [author, setAuthor] = useState('');
    const [isbn, setIsbn] = useState('');
    const [shelfLoc, setShelfLoc] = useState('');
    const [qty, setQty] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        let bookData = {
            title: title,
            author: author,
            isbn13: isbn,
            s_loc: shelfLoc,
            qty: Number(qty)
        }

        if (isNaN(Number(qty))) {
            alert('Enter valid number for quantity!');
            return;
        }

        const response = axios.post('/books', bookData).then((res) => alert('Book added!')).catch((err) => alert('Book already exists!'));
        setTitle('');
        setAuthor('');
        setIsbn('');
        setShelfLoc('');
        setQty('');
    }

    return <div className="add-book-container">
        <LeftNav/>
        <Card className="add-book-form">
            <h1 className="add-book-title">Add a new book</h1>
            <form className="add-book-form-container" onSubmit={handleSubmit}>
                <TextField className="add-book-textfield" label="Book Title" variant="standard" value={title} onChange={(e) => setTitle(e.target.value)} required />
                <TextField className="add-book-textfield" label="Author" variant="standard" value={author} onChange={(e) => setAuthor(e.target.value)} required />
                <TextField className="add-book-textfield" label="ISBN-13" variant="standard" value={isbn} onChange={(e) => setIsbn(e.target.value)} required />
                <TextField className="add-book-textfield" label="Shelf Location" variant="standard" value={shelfLoc} onChange={(e) => setShelfLoc(e.target.value)} required />
                <TextField className="add-book-textfield" label="Quantity" variant="standard" value={qty} onChange={(e) => setQty(e.target.value)} required />
                <Button className="add-book-button" variant="contained" color="primary" type="submit" >Add</Button>
            </form>
        </Card>
    </div>
}

export default AddBook;