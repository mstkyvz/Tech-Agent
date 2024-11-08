import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { PDFDownloadLink, Document, Page, Text, View, StyleSheet, Image, Font } from '@react-pdf/renderer';
import { Download } from 'lucide-react';
import ChatHistory from './ChatHistory';
import VideoModal from './VideoModel';
import ImagePreview from './ImagePreview';
import config from '../config.json'; 
import ReactMarkdown from 'react-markdown';

Font.register({
    family: 'Roboto',
    fonts: [
      {
        src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-light-webfont.ttf',
        fontWeight: 'normal',
      },
      {
        src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-bold-webfont.ttf',
        fontWeight: 'bold',
      },
    ],
  });
  
  const styles = StyleSheet.create({
    page: {
      padding: 30,
      backgroundColor: '#ffffff',
      fontFamily: 'Roboto',
    },
    message: {
      marginBottom: 20,
      padding: 10,
    },
    userMessage: {
      backgroundColor: '#f3f4f6',
      marginLeft: '20%',
    },
    assistantMessage: {
      backgroundColor: '#ffffff',
    },
    messageText: {
      fontSize: 12,
      lineHeight: 1.5,
      fontFamily: 'Roboto',
    },
    image: {
      marginBottom: 10,
      maxWidth: '100%',
      maxHeight: 200,
      objectFit: 'contain',
    },
    timestamp: {
      fontSize: 10,
      color: '#666666',
      marginTop: 5,
      fontFamily: 'Roboto',
    },
    // Markdown stilleri
    heading1: {
      fontSize: 18,
      fontWeight: 'bold',
      marginVertical: 10,
    },
    heading2: {
      fontSize: 16,
      fontWeight: 'bold',
      marginVertical: 8,
    },
    heading3: {
      fontSize: 14,
      fontWeight: 'bold',
      marginVertical: 6,
    },
    paragraph: {
      fontSize: 12,
      marginVertical: 4,
    },
    listItem: {
      fontSize: 12,
      marginLeft: 20,
    },
    code: {
      fontFamily: 'Courier',
      backgroundColor: '#f5f5f5',
      padding: 5,
      borderRadius: 3,
    },
    codeBlock: {
      fontFamily: 'Courier',
      backgroundColor: '#f5f5f5',
      padding: 10,
      marginVertical: 5,
      borderRadius: 5,
    },
  });
  
  // Markdown metni PDF için render eden bileşen
  const MarkdownText = ({ children }) => {
    const renderMarkdown = (text) => {
      return (
        <ReactMarkdown
          components={{
            h1: ({children}) => <Text style={styles.heading1}>{children}</Text>,
            h2: ({children}) => <Text style={styles.heading2}>{children}</Text>,
            h3: ({children}) => <Text style={styles.heading3}>{children}</Text>,
            p: ({children}) => <Text style={styles.paragraph}>{children}</Text>,
            li: ({children}) => <Text style={styles.listItem}>• {children}</Text>,
            code: ({inline, children}) => (
              <Text style={inline ? styles.code : styles.codeBlock}>
                {children}
              </Text>
            ),
          }}
        >
          {text}
        </ReactMarkdown>
      );
    };
  
    return <View>{renderMarkdown(children)}</View>;
  };
  

  // Helper function to detect if text contains markdown
  const containsMarkdown = (text) => {
    const markdownPatterns = [
      /^#+ /, // headers
      /\*\*.+\*\*/, // bold
      /\*.+\*/, // italic
      /```[\s\S]*?```/, // code blocks
      /`[^`]+`/, // inline code
      /^\s*[-*+] /, // unordered lists
      /^\s*\d+\. /, // ordered lists
      /\[.+\]\(.+\)/, // links
      /!\[.+\]\(.+\)/, // images
      /^\s*>.+/, // blockquotes
      /^\s*-{3,}/, // horizontal rules
      /\|.+\|.+\|/, // tables
    ];
  
    return markdownPatterns.some(pattern => pattern.test(text));
  };
  

  const markdownToPlainText = (markdown) => {
    return markdown
      .replace(/#{1,6} /g, '') // headers
      .replace(/\*\*/g, '') // bold
      .replace(/\*/g, '') // italic
      .replace(/```[\s\S]*?```/g, (match) => match.replace(/```/g, '')) // code blocks
      .replace(/`([^`]+)`/g, '$1') // inline code
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // links
      .replace(/!\[([^\]]+)\]\([^)]+\)/g, '$1') // images
      .replace(/^\s*[-*+] /gm, '') // unordered lists
      .replace(/^\s*\d+\. /gm, '') // ordered lists
      .replace(/^\s*>/gm, '') // blockquotes
      .replace(/^\s*-{3,}/gm, '') // horizontal rules
      .replace(/\|/g, ' ') // tables
      .trim();
  };
  
  const ChatPDF = ({ messages }) => (
    <Document>
      <Page size="A4" style={styles.page}>
        {messages.map((message, index) => (
          <View key={index} style={[
            styles.message,
            message.type === 'user' ? styles.userMessage : styles.assistantMessage
          ]}>
            {message.image && (
              <Image
                src={message.image}
                style={styles.image}
              />
            )}
            <MarkdownText>{message.content}</MarkdownText>
            <Text style={styles.timestamp}>
              {new Date(message.timestamp).toLocaleString('tr-TR')}
            </Text>
          </View>
        ))}
      </Page>
    </Document>
  );


const CreateQuestion = ({ onHistorySaved, initialChatHistory = [] }) => {
    const navigate = useNavigate();
    const { chatId } = useParams();
    const [selectedImage, setSelectedImage] = useState(null);
    const [selectedImageRender, setSelectedImageRender] = useState(null);
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState(() => {
        if (initialChatHistory.length > 0) {
            return initialChatHistory;
        }
        const saved = localStorage.getItem('chatHistory');
        
        return saved ? JSON.parse(saved) : [];
    });
    const [isLoading, setIsLoading] = useState(false);
    const [refreshingIndex, setRefreshingIndex] = useState(null);
    const chatEndRef = useRef(null);
    const [chatHistories, setChatHistories] = useState([]);

    useEffect(() => {
        const initializeChatId = async () => {
            if (!chatId && chatHistory.length === 0) {
                const newChatId = await getNextChatId();
                navigate(`/soruolustur/${newChatId}`);
            }
        };
        
        initializeChatId();
    }, [chatId, chatHistory, navigate]);

    useEffect(() => {
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }, [chatHistory]);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chatHistory]);

    useEffect(() => {
        fetchChatHistories();
    }, []);

    useEffect(() => {
        if (initialChatHistory.length > 0) {
            setChatHistory(initialChatHistory);
        }
    }, [initialChatHistory]);

    const handleImageChange = (e) => {
        const file = e.target.files ? e.target.files[0] : e.dataTransfer.files[0];
        if (file) {
            if (file.size > 5 * 1024 * 1024) { // 5MB limit
                alert("File size should not exceed 5MB");
                return;
            }
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
        e.currentTarget.classList.add('border-blue-500');
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.currentTarget.classList.remove('border-blue-500');
        handleImageChange(e);
    };

    const processStream = async (response, messageIndex = null) => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedResponse = '';

        try {
            while (true) {
                const { value, done } = await reader.read();

                if (done){
                    saveChatHistory();
                    break;
                }

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
        if (userMessage.image) {
           
            const response = await fetch(userMessage.image);
            const blob = await response.blob();
            formData.append('file', blob);
        }


        const previousMessages = chatHistory.slice(Math.max(0, index - 5), index); 
        formData.append('history', JSON.stringify(previousMessages));

        try {
            const response = await fetch(`${config.apiUrl}/chat_create_question/`, {
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
        if (!message && !selectedImage) {
            alert("Please enter a message or select an image.");
            return;
        }

        const userMessage = {
            type: 'user',
            content: message || '',
            image: selectedImageRender,
            timestamp: new Date().toISOString()
        };

        setChatHistory(prev => [...prev, userMessage]);

        const formData = new FormData();
        formData.append('message', message || '');
        if (selectedImage) {
            formData.append('file', selectedImage);
        }

        const lastMessages = chatHistory.slice(-5);
        formData.append('history', JSON.stringify(lastMessages));

        setIsLoading(true);

        try {
            const response = await fetch(`${config.apiUrl}/chat_create_question/`, {
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
            setSelectedImage(null);
            setSelectedImageRender(null);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    const fetchChatHistories = async () => {
        try {
            const response = await fetch(`${config.apiUrl}/get_all_histories/`);
            if (response.ok) {
                const histories = await response.json();
                setChatHistories(histories);
            }
        } catch (error) {
            console.error('Error fetching chat histories:', error);
        }
    };



    const saveChatHistory = async () => {
        if (chatHistory.length === 0) return;

        const autoTitle = chatId;
        const currentChatId = chatId ;

        try {
            const response = await fetch(`${config.apiUrl}/save_chat_history/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: autoTitle,
                    title: autoTitle,
                    messages: chatHistory
                }),
            });

            if (response.ok) {
                console.log('Chat history saved successfully!');
                if (onHistorySaved) {
                    onHistorySaved();
                }
                if (!chatId) {
                    const newChatId = await getNextChatId();
                    navigate(`/soruolustur/${newChatId}`);
                }
            } else {
                throw new Error('Failed to save chat history');
            }
        } catch (error) {
            console.error('Error saving chat history:', error);
        }
    };

    const clearChat = async () => {
        await saveChatHistory();
        setChatHistory([]);
        localStorage.removeItem('chatHistory');
        const newChatId = await getNextChatId();
        navigate(`/soruolustur/${newChatId}`);
    };

    const getNextChatId = async () => {
        try {
            const response = await fetch(`${config.apiUrl}/get_all_histories/`);
            if (response.ok) {
                const histories = await response.json();
                if (histories.length === 0) return '1';
                const numericIds = histories
                    .map(history => parseInt(history.id))
                    .filter(id => !isNaN(id));
                const maxId = Math.max(...numericIds, 0);
                return (maxId + 1).toString();
            }
            return '1';
        } catch (error) {
            console.error('Error fetching histories:', error);
            return '1';
        }
    };

    const ExportButton = () => (
        <div className="absolute top-4 right-0 md:right-4">
          <PDFDownloadLink
            document={<ChatPDF messages={chatHistory} />}
            fileName={`chat-${chatId}.pdf`}
            className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-1 px-2 rounded-full flex items-center justify-center group"
          >
            {({ blob, url, loading, error }) => (
              <div className="flex items-center gap-1">
                {loading ? (
                  'Loading...'
                ) : (
                  <>
                    <Download size={16} />
                  </>
                )}
              </div>
            )}
          </PDFDownloadLink>
        </div>
      );
    return (
        <div className='relative flex flex-col w-full flex-1 justify-start items-center'>
            <div className='z-50 absolute right-0  border-r-8'>
            <ExportButton />
            </div>
            <div className="mx-auto flex-1 w-full items-start justify-center overflow-y-auto mb-48">
            <div className="flex w-full md:px-10">
                    <ChatHistory 
                        messages={chatHistory} 
                        onRefreshMessage={handleRefreshMessage}
                    />
                </div>
                <div ref={chatEndRef} />
            </div>
            <div className="flex flex-col items-center w-full md:w-4/5 absolute bottom-0 bg-opacity-60">
            <ImagePreview selectedImageRender={selectedImageRender} />
                <div className="flex flex-col items-center mt-2 mb-5 w-11/12 md:w-3/5">
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
                                        <span className="font-semibold">Drag & drop or click here to upload an image of your problem</span>
                                    </p>
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
                        <div className="w-1/12 mr-10 md:mr-2">
                        <button
                            onClick={clearChat}
                            className="bg-gray-500 hover:bg-gray-600 text-white text-sm font-bold py-[10px] px-4 rounded"
                        >
                            Yeni
                        </button>
                    </div>
                    </div>
                </div>
            </div>
            <div className="flex items-center justify-center md:h-48 right-0 m-2 absolute mt-14 md:mt-0 md:bottom-0 rounded-3xl">
            <div className='flex items-center justify-center  w-8 h-8 md:w-24 md:h-24'>
           <VideoModal id={`${chatId}`} saveChatHistory={saveChatHistory}/>        
           </div>

           </div>

        </div>

    );
};

export default CreateQuestion;