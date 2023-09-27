import React, { useEffect, useState } from "react";
import axios from "../axiosConfig";
import LeftNav from "./LeftNav";
import { Button, Card, Dialog, DialogContent, DialogTitle, TextField } from "@mui/material";
import './ViewBooks.css';
import { useSelector } from "react-redux";

const ViewBooks = () => {

    const [books, setBooks] = useState();
    const [open, setOpen] = useState(false);
    const [bo, setBo] = useState();
    const [title, setTitle] = useState('');
    const [author, setAuthor] = useState('');
    const [isbn13, setIsbn13] = useState('');
    const [sLoc, setSLoc] = useState('');
    const [qty, setQty] = useState('');
    const [id, setId] = useState();

    const userData = useSelector(
        (state) => state.user.user
    );

    const handleClickOpen = (book) => {
        setOpen(true);
        setBo(book);
        setId(book.id)
        setTitle(book.title);
        setAuthor(book.author);
        setIsbn13(book.isbn13);
        setSLoc(book.s_loc);
        setQty(book.qty);
    }

    const handleClickClose = () => {
        setOpen(false);
    }

    const getAllBooks = () => {
        const response = axios.get('/books').then((res) => setBooks(res.data)).catch((err) => console.error(err));
    }

    useEffect(() => {
        getAllBooks();
    }, [open]);

    const handleSubmit = (e) => {
        e.preventDefault();
        let editedDetail = {
            title: title,
            author: author,
            isbn13: isbn13,
            s_loc: sLoc,
            qty: Number(qty)
        }

        const response = axios.put(`/books/${bo.id}`, editedDetail).then((res) => console.log(res)).catch((err) => console.error(err));
        handleClickClose();
    }

    const handleDelete = (book) => {
        const response = axios.delete(`/books/${book.id}`).then((res) => {
            console.log(res);
            getAllBooks();
        }).catch((err) => console.error(err));
    }

    return <div className="view-books-container">
        <LeftNav/>
        <div className="view-book-card">
            <h1 className="view-book-title">All Books</h1>
            <table className="view-book-table">
                <thead>
                    <tr>
                        <th className="view-book-expand">Book Title</th>
                        <th className="view-book-expand">Author</th>
                        <th>ISBN-13</th>
                        {userData.role == 'admin' ? <th>Shelf Location</th> : ""}
                        <th>Quantity</th>
                        {userData.role == 'admin' ? <th>Action</th> : ""}
                    </tr>
                </thead>
                <tbody>
                    {
                        books?.map((book, i) => {
                            return (
                                <tr key={i}>
                                    <td>{book.title}</td>
                                    <td>{book.author}</td>
                                    <td>{book.isbn13}</td>
                                    {userData.role == 'admin' ? <td>{book.s_loc}</td> : ""}
                                    <td>{book.qty}</td>
                                    {userData.role == 'admin' ? <td>
                                        <Button onClick={() => handleClickOpen(book)}>Edit</Button>
                                        <Dialog fullWidth open={open} onClose={handleClickClose}>
                                            <DialogTitle className="edit-book-title">Edit Book Details</DialogTitle>
                                            <DialogContent>
                                                <form onSubmit={handleSubmit} className="edit-book-form">
                                                    <TextField className="edit-book-textfield" label="Book Title" variant="standard" value={title} onChange={(e) => setTitle(e.target.value)} required />
                                                    <TextField className="edit-book-textfield" label="Author" variant="standard" value={author} onChange={(e) => setAuthor(e.target.value)} required />
                                                    <TextField className="edit-book-textfield" label="ISBN-13" variant="standard" value={isbn13} onChange={(e) => setIsbn13(e.target.value)} required />
                                                    <TextField className="edit-book-textfield" label="Shelf Location" variant="standard" value={sLoc} onChange={(e) => setSLoc(e.target.value)} required />
                                                    <TextField className="edit-book-textfield" label="Quantity" variant="standard" value={qty} onChange={(e) => setQty(e.target.value)} required />
                                                    <Button className="edit-book-button" variant="contained" color="primary" type="submit">Edit</Button>
                                                </form>
                                            </DialogContent>
                                        </Dialog>
                                        <Button onClick={() => handleDelete(book)}>Delete</Button>
                                    </td> : ""}
                                </tr>
                            );
                        })
                    }
                </tbody>
            </table>
        </div>
    </div>
}

export default ViewBooks;