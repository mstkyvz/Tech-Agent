import React, { useState, useEffect } from 'react';
import ChatHistory from './ChatHistory';

const QuestionArea = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [selectedImageRender, setSelectedImageRender] = useState(null);
    const [responses, setResponses] = useState([]);
    const [message, setMessage] = useState('');

    const handleImageChange = (e) => {
        const file = e.target.files ? e.target.files[0] : e.dataTransfer.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setSelectedImageRender(reader.result);
            };
            reader.readAsDataURL(file);
            setSelectedImage(file);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        handleImageChange(e);
    };

    const handleSendMessage = async () => {
        if (!message && !selectedImage) {
            alert("Please enter a message or select an image.");
            return;
        }

        const formData = new FormData();
        formData.append('message', message);
        if (selectedImage) {
            formData.append('file', selectedImage);
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/upload/', {
                method: 'POST',
                body: formData,
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let accumulatedResponse = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                setResponses(prev => [...prev, chunk]);

            }


        } catch (error) {
            console.error("Error sending data:", error);
        }
    };



    return (
        <div className='flex flex-col w-full flex-1 justify-start items-center overflow-y-auto'>
            <ChatHistory selectedImage={selectedImageRender} messages={responses} />
            <div className="flex flex-col items-center w-4/5 absolute bottom-0 bg-opacity-60 ">
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
                                    <p className="mb-2 text-sm text-gray-500 dark:text-gray-400"><span className="font-semibold">Drag & drop or click here to upload an image of your problem</span></p>
                                    <p className="text-xs text-gray-500 dark:text-gray-400">PNG, JPG or JPEG</p>
                                </div>
                                <input id="dropzone-file" type="file" className="hidden" onChange={handleImageChange} />
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
                        />
                        <button
                            className="shadow-cr mx-1 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-2 rounded-md"
                            onClick={handleSendMessage}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="m5 12 7-7 7 7"></path>
                                <path d="M12 19V5"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QuestionArea;