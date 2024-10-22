import React, { useState, useEffect } from 'react';
import Latex from 'react-latex-next';

const ChatHistory = ({ selectedImage, messages }) => {
    const [m, setMessage] = useState("");

    useEffect(() => {
        let combinedMessage = "";
        messages.forEach((msg) => {
            combinedMessage += msg;
        });
        setMessage(combinedMessage);
    }, [messages]);

    return (
        <div className='flex flex-col h-full w-full justify-start items-center mb-48 overflow-y-auto'>
            {selectedImage && (
                <div className="flex flex-col md:flex-row justify-center items-center gap-4 w-4/5 my-4">
                    <div className="bg-white p-4 rounded-lg shadow-cr w-full flex flex-col justify-between">
                        <div className='h-full overflow-y-auto'>
                            <img src={selectedImage} alt="Uploaded" className="h-full object-contain" />
                        </div>
                    </div>
                </div>
            )}
            {m.length > 1 ? (
                <div className="flex flex-col md:flex-row justify-center items-center gap-4 w-4/5 my-4">
                    <div className="bg-white p-4 rounded-lg shadow-cr w-full flex flex-col justify-between">
                        <div className='overflow-y-auto text-center relative'>
                            <Latex>
                                {m}
                            </Latex>
                        </div>
                    </div>
                </div>) : (<></>)}
        </div>
    );
};

export default ChatHistory;
