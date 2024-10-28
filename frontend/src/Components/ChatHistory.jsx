import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import 'katex/dist/katex.min.css';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';
import { RotateCw } from 'lucide-react';

const ChatHistory = ({ messages, onRefreshMessage }) => {
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const MarkdownComponents = {
        p: ({ children }) => <p className="mb-4 text-gray-800">{children}</p>,
        h1: ({ children }) => <h1 className="text-2xl font-bold mb-4">{children}</h1>,
        h2: ({ children }) => <h2 className="text-xl font-bold mb-3">{children}</h2>,
        h3: ({ children }) => <h3 className="text-lg font-bold mb-2">{children}</h3>,
        code: ({ node, inline, children }) => (
            inline ? 
                <code className="bg-gray-100 px-1 rounded">{children}</code> :
                <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto mb-4">
                    <code>{children}</code>
                </pre>
        ),
        ul: ({ children }) => <ul className="list-disc pl-6 mb-4">{children}</ul>,
        ol: ({ children }) => <ol className="list-decimal pl-6 mb-4">{children}</ol>,
        a: ({ href, children }) => (
            <a href={href} className="text-gray-200 hover:underline" target="_blank" rel="noopener noreferrer">
                {children}
            </a>
        ),
        blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-gray-100 pl-4 italic my-4">
                {children}
            </blockquote>
        ),
    };

    return (
        <div className="flex flex-col w-full h-full p-4 space-y-4 overflow-y-auto">
            {messages.map((message, index) => (
                <div 
                    key={index} 
                    className={`flex  w-full ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                    <div 
                        className={`relative  max-w-[70%] rounded-lg p-6 shadow-md
                            ${message.type === 'user' 
                                ? 'bg-gray-200 text-black ml-auto rounded-br-none' 
                                : message.type === 'error' 
                                    ? 'bg-red-100 text-red-800 mr-auto rounded-bl-none' 
                                    : 'bg-white text-black mr-auto rounded-bl-none'
                            }`}
                    >
                        {message.type !== 'user' && (
                            <button
                                onClick={() => onRefreshMessage(index)}
                                className="absolute top-2 right-2 p-1  rounded-full hover:bg-gray-200 transition-colors"
                                title="Refresh response"
                            >
                                <RotateCw size={16} className="text-gray-600" />
                            </button>
                        )}
                        {message.image && (
                            <div className="mb-4">
                                <img 
                                    src={message.image} 
                                    alt="Uploaded" 
                                    className="max-h-64 w-full object-contain rounded"
                                    loading="lazy"
                                />
                            </div>
                        )}
                        <div className={`prose prose-sm max-w-none ${message.type === 'user' ? 'text-black' : ''}`}>
                            {message.type === 'user' ? (
                                <p className="whitespace-pre-wrap break-words">{message.content}</p>
                            ) : (
                                <ReactMarkdown
                                    remarkPlugins={[remarkMath, remarkGfm]}
                                    rehypePlugins={[rehypeKatex]}
                                    components={MarkdownComponents}
                                    className="break-words"
                                >
                                    {message.content}
                                </ReactMarkdown>
                            )}
                        </div>
                    </div>
                </div>
            ))}
            <div ref={messagesEndRef} />
        </div>
    );
};

export default ChatHistory;