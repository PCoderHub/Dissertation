import React, { useEffect, useState } from 'react';
import LeftNav from './LeftNav';
import axios from "../axiosConfig";
import './ReturnBooks.css';
import { Button, Dialog, DialogContent, DialogTitle, TextField } from '@mui/material';
import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

const ReturnBooks = () => {

    const [issues, setIssues] = useState();
    const [books, setBooks] = useState();
    const [open, setOpen] = useState(false);
    const [mem, setMem] = useState();
    const [bo, setBo] = useState();
    const [idate, setIdate] = useState();
    const [rdate, setRdate] = useState();
    const [udate, setUdate] = useState('');
    const [iss, setIss] = useState();
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    const getIssues = () => {
        const response = axios.get('/issues').then((res) => setIssues(res.data)).catch((err) => console.error(err));
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

    const getDefaulters = () => {
        issues?.forEach((issue) => {
            if (new Date(issue.rdate) < new Date() && issue.status == 'pending') {
                let editedIssue = {
                    book: issue.book,
                    member: issue.member,
                    idate: issue.idate,
                    rdate: issue.rdate,
                    actret: issue.actret,
                    status: 'defaulter'
                };
                const response = axios.put(`/issues/${issue.id}`, editedIssue).then((res) => console.log(res)).catch((err) => console.error(err));
            }
        });
        getIssues();
        const memberFine = {};
        issues?.filter(issue => (issue.status == 'defaulter' || issue.status == 'returned with delay' || issue.status == 'dues paid, not returned')).forEach((defaulter) => {
            const fine = defaulter.status == 'returned with delay' ? Math.floor(Math.abs(new Date(defaulter.actret).getTime() - new Date(defaulter.rdate).getTime())/(1000*3600*24)) : Math.floor(Math.abs(new Date().getTime() - new Date(defaulter.rdate).getTime())/(1000*3600*24));
            if (memberFine.hasOwnProperty(defaulter.member)) {
                memberFine[defaulter.member] = memberFine[defaulter.member] + fine
            } else {
                memberFine[defaulter.member] = fine
            }
        })
        Object.entries(memberFine).map(([member, due]) => {
            const r = axios.post('/defaulter', {
                member: member,
                dues: due,
                status: 'unpaid'
            }).then((res) => console.log(res)).catch((err) => console.log(err));
        })
    }

    useEffect(() => {
        getIssues();
        getBooks();
    }, [open]);

    const handleClickOpen = (issue) => {
        setOpen(true);
        setIss(issue);
        setBo(issue.book);
        setMem(issue.member);
        setIdate(issue.idate);
        setRdate(issue.rdate);
        setUdate(issue.actret);
    }

    const handleClickClose = () => {
        setOpen(false);
        getDefaulters();
    }

    const handleEdit = (e) => {
        e.preventDefault();
        const irdate = new Date(rdate);
        const ardate = new Date(udate);
        let editedDetail = {};

        if (udate != '') {
            if (irdate >= ardate) {
                editedDetail = {
                    book: bo,
                    member: mem,
                    idate: idate,
                    rdate: rdate,
                    actret: udate,
                    status: 'returned'
                }
            } else {
                editedDetail = {
                    book: bo,
                    member: mem,
                    idate: idate,
                    rdate: rdate,
                    actret: udate,
                    status: 'returned with delay'
                }
            }
    
            const response = axios.put(`/issues/${iss.id}`,editedDetail).then((res) => {
                console.log(res);
                const bookDetail = axios.get(`/books/${res.data.book}`).then((respo) => {
                    let bookDetail = {
                        title: respo.data.title,
                        author: respo.data.author,
                        isbn13: respo.data.isbn13,
                        s_loc: respo.data.s_loc,
                        qty: respo.data.qty + 1
                    }
                    const resp = axios.put(`/books/${res.data.book}`, bookDetail).then((res) => console.log(res)).catch((err) => console.error(err));
                })
            }).catch((err) => alert(err.response.data.message));
        }

        setBo('');
        setMem('');
        setIdate('');
        setUdate('');
        handleClickClose();
    }

    const handleReport = (e) => {
        e.preventDefault();
        let data = [];
        const response = axios.get('/generatereport', {
            params : {
                startdate: startDate,
                enddate: endDate
            }
        }).then((res) => {
            res.data?.forEach((item) => {
                data.push([getTitle(item.book), item.member, item.idate, item.rdate, item.actret, item.status]);
            });
            console.log(`Data array is ${data}`);
            let pdf = new jsPDF();
            autoTable(pdf, {
                head: [['Book', 'Member', 'Issue Date', 'Return Date', 'Actual Return', 'Status']],
                body: data
            })

            pdf.save(`report_${startDate}-${endDate}.pdf`);
            }).catch((err) => console.error(err));
        setStartDate('');
        setEndDate('');
    }

    return <div className='return-book-container'>
        <LeftNav/>
        <div className='return-book-card'>
        <form onSubmit={handleReport}>
            <TextField label="Start Date" type="date" sx={{margin: '5px', width: 200}} value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
            <TextField label="End Date" type="date" sx={{margin: '5px', width: 200}} value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
            <Button variant="contained" color="primary" type="submit" sx={{margin: '10px', width: 200}} >Generate PDF</Button>
        </form>
            <Button className='refresh-button' onClick={getDefaulters}>Refresh</Button>
            <h1 className='return-book-title'>Report</h1>
            <table className='return-book-table'>
                <thead>
                    <tr>
                        <th>Member</th>
                        <th className='return-book-expand'>Book</th>
                        <th>Issue Date</th>
                        <th>To be returned</th>
                        <th>Actual Return</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        issues?.map((issue, i) => {
                            return (
                                <tr key={i}>
                                    <td>{issue.member}</td>
                                    <td>{getTitle(issue.book)}</td>
                                    <td>{issue.idate}</td>
                                    <td>{issue.rdate}</td>
                                    <td>{issue.actret}</td>
                                    <td>{issue.status}</td>
                                    <td>
                                        <Button onClick={() => handleClickOpen(issue)}>Update</Button>
                                        <Dialog fullWidth open={open} onClose={handleClickClose}>
                                            <DialogTitle className='return-edit-title'>Update Record</DialogTitle>
                                            <DialogContent>
                                                <form onSubmit={handleEdit} className='return-edit-form'>
                                                    <TextField className='return-edit-textfield' label='Member' value={mem} disabled />
                                                    <TextField className='return-edit-textfield' label='Book' value={getTitle(bo)} disabled />
                                                    <TextField className='return-edit-textfield' label='Issue Date' type='date' value={idate} disabled />
                                                    <TextField className='return-edit-textfield' label='To be returned' type='date' value={rdate} disabled />
                                                    <TextField className='return-edit-textfield' label='Actual Return Date' type='date' value={udate} onChange={(e) => setUdate(e.target.value)} required/>
                                                    <Button className='return-edit-button' type='submit'>Edit</Button>
                                                </form>
                                            </DialogContent>
                                        </Dialog>
                                    </td>
                                </tr>
                            );
                        })
                    }
                </tbody>
            </table>
        </div>
    </div>
}

export default ReturnBooks;