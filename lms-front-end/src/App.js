import React from 'react';
import './App.css';
import { Route, Routes } from 'react-router-dom';
import Layout from './Layout';
import Landing from './components/Landing';
import AddBook from './components/AddBook';
import ViewBooks from './components/ViewBooks';
import ViewMembers from './components/ViewMembers';
import IssueBooks from './components/IssueBooks';
import ReturnBooks from './components/ReturnBooks';
import Defaulter from './components/Defaulter';
import Home from './components/Home';
import Borrowed from './components/Borrowed';
import FinePayment from './components/FinePayment';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe('pk_test_51NTPZSKPLgEWMpSqBLgc75HzhCmVMY5guoEZpmZutnr4He0apfkIp3lORAZDKlY9kjrI4ygCLCbPiADArr66EKEX00uBus5q0f');

function App() {
  return (
    <div className='App'>
      <Routes>
        <Route path='/' element={<Layout/>}>
          <Route path='/' element={<Landing stripePromise={stripePromise} />}></Route>
          <Route path='/home' element={<Home/>}></Route>
          <Route path='/add-book' element={<AddBook/>}></Route>
          <Route path='/view-book' element={<ViewBooks/>} ></Route>
          <Route path='/view-members' element={<ViewMembers/>} ></Route>
          <Route path='/issue-books' element={<IssueBooks/>} ></Route>
          <Route path='/issued-status' element={<ReturnBooks/>}></Route>
          <Route path='/defaulter-list' element={<Defaulter/>}></Route>
          <Route path='/borrowed' element={<Borrowed/>}></Route>
          <Route path='/fine' element={<Elements stripe={stripePromise}><FinePayment/></Elements>}></Route>
        </Route>
      </Routes>
    </div>
  );
}

export default App;
