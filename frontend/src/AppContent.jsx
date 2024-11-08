import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Navbar from './Components/Navbar';
import Sidebar from './Components/Sidebar';
import QuestionArea from './Components/QuestionArea';
import KonuAnlatim from './Components/KonuAnlatim';
import PodCast from './Components/PodCast';
import './App.css';
import CreateQuestion from './Components/CreateQuestion';

import config from './config.json';
import MainPage from './Components/MainPage';

const AppContent = () => {
    const [isOpen, setIsOpen] = useState(true);
    const [chatHistories, setChatHistories] = useState([]);
    const [currentChatHistory, setCurrentChatHistory] = useState(null);
    const navigate = useNavigate();
    const toggleSidebar = () => setIsOpen(!isOpen);
    
    useEffect(() => {
        fetchChatHistories();
    }, []);

    const fetchChatHistories = async () => {
        try {
            const response = await fetch(`${config.apiUrl}/get_all_histories/`);
            if (response.ok) {
                const data = await response.json();
                setChatHistories(data);
            }
        } catch (error) {
            console.error('Error fetching chat histories:', error);
        }
    };

    const handleHistorySelect = async (historyId) => {
        try {
            const response = await fetch(`${config.apiUrl}/get_chat_history/${historyId}`);
            if (response.ok) {
                const history = await response.json();
                setCurrentChatHistory(history);
                navigate(`/soru/${historyId}`);
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    };

    return (
        <div className="flex flex-col">
            <Navbar toggleSidebar={toggleSidebar} />
            <div className="flex h-[calc(100vh-66px)]">
                <Sidebar
                    isOpen={isOpen}
                    chatHistories={chatHistories}
                    onHistorySelect={handleHistorySelect}
                />
                <div className="flex w-full bg-[#f9faff]">
                    <Routes>
                        <Route
                            path="/"
                            element={
                                <MainPage/>
                            }
                        />
                        <Route
                            path="/konu"
                            element={
                                <KonuAnlatim onHistorySaved={fetchChatHistories} />
                            }
                        />
                        <Route
                            path="/konu/:chatId"
                            element={
                                <KonuAnlatim
                                    onHistorySaved={fetchChatHistories}
                                    initialChatHistory={currentChatHistory?.messages || []}
                                />
                            }
                        />
                        <Route
                            path="/soru"
                            element={
                                <QuestionArea onHistorySaved={fetchChatHistories} />
                            }
                        />
                        <Route
                            path="/soru/:chatId"
                            element={
                                <QuestionArea
                                    onHistorySaved={fetchChatHistories}
                                    initialChatHistory={currentChatHistory?.messages || []}
                                />
                            }
                        />
                        <Route
                            path="/soruolustur"
                            element={
                                <CreateQuestion onHistorySaved={fetchChatHistories} />
                            }
                        />
                        <Route
                            path="/soruolustur/:chatId"
                            element={
                                <CreateQuestion
                                    onHistorySaved={fetchChatHistories}
                                    initialChatHistory={currentChatHistory?.messages || []}
                                />
                            }
                        />
                        <Route
                            path="/podcast"
                            element={<PodCast />}
                        />
                    </Routes>
                </div>
            </div>
        </div>
    );
};

export default AppContent;
