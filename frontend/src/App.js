import React, { useState } from 'react';
import Navbar from './Components/Navbar';
import Content from './Components/Content';
import Sidebar from './Components/Sidebar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';

function App() {

  const [isOpen, setIsOpen] = useState(true);
  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <Router>
      <div className="flex flex-col">
        <Navbar toggleSidebar={toggleSidebar} />
        <div className="flex h-[calc(100vh-66px)]">
          <Sidebar isOpen={isOpen} />
          <Routes>
          <Route path="/" element={<div></div> } />
          <Route path="/soru" element={ <Content />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
