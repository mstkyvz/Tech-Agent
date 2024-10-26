import React, { useState, useRef, useEffect } from 'react';
import ChatHistory from './ChatHistory';

const KonuAnlatim = () => {
    const [selectedPDF, setSelectedPDF] = useState(null);
    const [pdfName, setPdfName] = useState('');
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState(() => {
        const saved = localStorage.getItem('chatHistory');
        return saved ? JSON.parse(saved) : [];
    });
    const [isLoading, setIsLoading] = useState(false);
    const [refreshingIndex, setRefreshingIndex] = useState(null);
    const chatEndRef = useRef(null);

    useEffect(() => {
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }, [chatHistory]);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chatHistory]);

    const handlePDFChange = (e) => {
        const file = e.target.files ? e.target.files[0] : e.dataTransfer.files[0];
        if (file) {
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                alert("File size should not exceed 10MB");
                return;
            }
            if (file.type !== 'application/pdf') {
                alert("Please upload a PDF file");
                return;
            }
            setSelectedPDF(file);
            setPdfName(file.name);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.currentTarget.classList.add('border-blue-500');
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.currentTarget.classList.remove('border-blue-500');
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.currentTarget.classList.remove('border-blue-500');
        handlePDFChange(e);
    };

    const processStream = async (response, messageIndex = null) => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedResponse = '';

        try {
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value);
                accumulatedResponse += chunk;

                setChatHistory(prev => {
                    const newHistory = [...prev];
                    const updateIndex = messageIndex !== null ? messageIndex : newHistory.length - 1;
                    if (updateIndex >= 0) {
                        newHistory[updateIndex] = {
                            ...newHistory[updateIndex],
                            content: accumulatedResponse
                        };
                    }
                    return newHistory;
                });
            }
        } catch (error) {
            console.error('Error processing stream:', error);
            throw error;
        }
    };

    const handleRefreshMessage = async (index) => {
        if (isLoading || refreshingIndex !== null) return;
        
        setRefreshingIndex(index);
        
        const userMessage = chatHistory[index - 1]; 
        if (!userMessage) return;

        const formData = new FormData();
        formData.append('message', userMessage.content || '');
        if (userMessage.pdf) {
            const response = await fetch(userMessage.pdf);
            const blob = await response.blob();
            formData.append('file', blob, 'document.pdf');
        }

        const previousMessages = chatHistory.slice(Math.max(0, index - 5), index); 
        formData.append('history', JSON.stringify(previousMessages));

        try {
            const response = await fetch('http://127.0.0.1:8000/chat_konu/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            await processStream(response, index);

        } catch (error) {
            console.error("Error:", error);
            setChatHistory(prev => {
                const newHistory = [...prev];
                newHistory[index] = {
                    type: 'error',
                    content: error.message,
                    timestamp: new Date().toISOString()
                };
                return newHistory;
            });
        } finally {
            setRefreshingIndex(null);
        }
    };

    const handleSendMessage = async () => {
        if (!message && !selectedPDF) {
            alert("Please enter a message or select a PDF file.");
            return;
        }

        const userMessage = {
            type: 'user',
            content: message || '',
            pdf: selectedPDF ? URL.createObjectURL(selectedPDF) : null,
            pdfName: pdfName,
            timestamp: new Date().toISOString()
        };

        setChatHistory(prev => [...prev, userMessage]);

        const formData = new FormData();
        formData.append('message', message || '');
        if (selectedPDF) {
            formData.append('file', selectedPDF, selectedPDF.name);
        }

        const lastMessages = chatHistory.slice(-5);
        formData.append('history', JSON.stringify(lastMessages));

        setIsLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/chat_konu/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            setChatHistory(prev => [...prev, {
                type: 'assistant',
                content: '',
                timestamp: new Date().toISOString()
            }]);

            await processStream(response);

        } catch (error) {
            console.error("Error:", error);
            setChatHistory(prev => [...prev, {
                type: 'error',
                content: error.message,
                timestamp: new Date().toISOString()
            }]);
        } finally {
            setIsLoading(false);
            setMessage('');
            setSelectedPDF(null);
            setPdfName('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const clearChat = () => {
        if (window.confirm('Are you sure you want to clear the chat history?')) {
            setChatHistory([]);
            localStorage.removeItem('chatHistory');
        }
    };

    return (
        <div className='relative flex flex-col w-full flex-1 justify-start items-center'>
            <div className="mx-auto flex-1 w-full items-start justify-center overflow-y-auto mb-48">
                <div className="flex w-full px-10">
                    <ChatHistory 
                        messages={chatHistory} 
                        onRefreshMessage={handleRefreshMessage}
                    />
                    <button
                        onClick={clearChat}
                        className="absolute top-4 right-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                    >
                        Clear Chat
                    </button>
                </div>
                <div ref={chatEndRef} />
            </div>
            <div className="flex flex-col items-center w-4/5 absolute bottom-0 bg-opacity-60">
                <div className="flex flex-col items-center mt-2 mb-5 w-3/5">
                    <div className="bg-white rounded-lg w-full h-2/12 md:h-[100px]"
                        onDragOver={handleDragOver}
                        onDrop={handleDrop}>
                        <div className="flex items-center justify-center w-full h-full">
                            <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-full border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 hover:border-blue-400">
                                <div className="flex flex-col items-center justify-center pt-8 pb-8">
                                    <svg className="w-8 h-8 mb-2 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                                        <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
                                    </svg>
                                    <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                                        <span className="font-semibold">
                                            {pdfName ? `Selected: ${pdfName}` : 'Drag & drop or click here to upload a PDF file'}
                                        </span>
                                    </p>
                                    <p className="text-xs text-gray-500 dark:text-gray-400">PDF files only (max 10MB)</p>
                                </div>
                                <input 
                                    id="dropzone-file" 
                                    type="file" 
                                    className="hidden" 
                                    onChange={handlePDFChange}
                                    accept=".pdf"
                                />
                            </label>
                        </div>
                    </div>
                    <div className="flex items-center w-full mt-1">
                        <input
                            type="text"
                            className="shadow-cr border border-gray-300 rounded-md px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Type your question here..."
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            onKeyPress={handleKeyPress}
                            disabled={isLoading}
                        />
                        <button
                            className={`shadow-cr mx-1 ${isLoading ? 'bg-gray-400' : 'bg-gray-500 hover:bg-gray-700'} text-white font-bold py-2 px-2 rounded-md`}
                            onClick={handleSendMessage}
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            ) : (
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="m5 12 7-7 7 7"></path>
                                    <path d="M12 19V5"></path>
                                </svg>
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default KonuAnlatim;