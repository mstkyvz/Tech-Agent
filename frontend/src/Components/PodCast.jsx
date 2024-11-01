import React, { useState, useRef } from 'react';
import axios from 'axios';
import config from '../config.json'; 

const Podcast = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const audioRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files ? e.target.files[0] : e.dataTransfer.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        alert("Please upload only PDF files");
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add('bg-blue-100', 'border-blue-500');
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('bg-blue-100', 'border-blue-500');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('bg-blue-100', 'border-blue-500');
    handleFileSelect(e);
  };

  const handleSendPDF = async () => {
    if (!selectedFile) {
      alert('Please select a PDF file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setIsLoading(true);

    try {
      const response = await axios.post(`${config.apiUrl}/upload-pdf/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      const audioFileName = response.data.audio_file.split('/').pop();
      setAudioFile(`${config.apiUrl}/audio/${audioFileName}`);
    } catch (error) {
      console.error('Error uploading PDF:', error);
      alert('An error occurred while uploading the PDF');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlay = () => {
    if (audioRef.current) {
      audioRef.current.play();
    }
  };

  const handlePause = () => {
    if (audioRef.current) {
      audioRef.current.pause();
    }
  };

  const handleClick = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf';
    input.onchange = handleFileSelect;
    input.click();
  };

  return (
    <div className="flex flex-col justify-center items-center w-full h-full">
      <div className="flex flex-col justify-center items-center rounded-3xl bg-white h-3/4 w-1/2 shadow-2xl p-8  mx-auto">
        <h2 className="text-6xl  font-bold mb-10 ">Podcast</h2>
        
        <button
          onClick={handleClick}
          disabled={isLoading}
          className="w-full mb-4 p-6 border-2 border-gray-300 border-dashed rounded-lg 
            hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 
            transition-colors duration-200 ease-in-out"
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center justify-center">
            <svg className="w-8 h-8 mb-2 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
              <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
            </svg>
            <p className="text-sm text-gray-500 font-semibold">
              Click or drag and drop PDF here
            </p>
          </div>
        </button>

        <button 
          onClick={handleSendPDF}
          disabled={!selectedFile || isLoading}
          className={`w-full px-4 py-2 rounded mb-4 ${
            !selectedFile || isLoading 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-500 text-white hover:bg-blue-600'
          }`}
        >
          {isLoading ? 'Uploading...' : 'Upload'}
        </button>

        {selectedFile && (
          <div className="w-full mb-4">
            <p className="text-sm text-gray-500">Selected file: {selectedFile.name}</p>
          </div>
        )}

        {isLoading && (
          <div className="flex justify-center items-center mb-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>
        )}

        {audioFile && (
          <div className="flex flex-col space-y-4 w-full">
            <audio 
              ref={audioRef} 
              src={audioFile} 
              className="w-full"
              controls
            />
            
          </div>
        )}
      </div>
    </div>
  );
};

export default Podcast;