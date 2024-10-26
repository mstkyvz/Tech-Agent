import React, { useState } from 'react';
import Navbar from './Components/Navbar';
import Content from './Components/Content';
import Sidebar from './Components/Sidebar';
import QuestionArea from './Components/QuestionArea';
import KonuAnlatim from './Components/KonuAnlatim';
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
          <div className="flex w-full bg-[#f9faff]">
          <Routes>


            <Route path="/" element={<KonuAnlatim />} />
            <Route path="/soru" element={<QuestionArea />} />
            <Route path="/konu" element={<KonuAnlatim />} />
          </Routes>
        </div>
      </div>
      </div>
    </Router >
  );
}

export default App;
