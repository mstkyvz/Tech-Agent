import React from 'react';
import { MessageSquare, Settings, Book, PenTool, MessageCircle } from 'lucide-react';

const Sidebar = ({ isOpen, chatHistories = [], onHistorySelect }) => {
    return (
        <div className="relative">
            <aside className={`${isOpen ? 'w-56' : 'w-0'} h-full bg-white transition-all duration-300 ease-in-out overflow-hidden`}>
                <ul className="menu w-56 flex flex-col h-full py-4">
                    <li>
                        <a href='/konu' className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
                            <Book size={18} />
                            Konu Anlatım
                        </a>
                    </li>
                    <li>
                        <a href='/soru' className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
                            <PenTool size={18} />
                            Soru Çöz
                        </a>
                    </li>
                    <li>
                        <a href='/sorucoz' className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
                            <MessageSquare size={18} />
                            Soru Oluştur
                        </a>
                    </li>
                    <li>
                        <a href='/podcast' className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
                            <MessageCircle size={18} />
                            Tartışma
                        </a>
                    </li>
                    
                    {chatHistories.length > 0 && (
                        <li className="mt-4">
                            <span className="text-sm text-gray-500 px-4 py-2 block">
                                Saved Questions
                            </span>
                            <ul className="mt-2 overflow-y-auto">
                                {chatHistories.map((history) => (
                                    <li key={history.id}>
                                        <button
                                            onClick={() => onHistorySelect(history.id)}
                                            className="w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                                        >
                                            Chat-{history.title}
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </li>
                    )}
                    
                    <li className="mt-auto">
                        <a className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
                            <Settings size={18} />
                            Ayarlar
                        </a>
                    </li>
                </ul>
            </aside>
        </div>
    );
};

export default Sidebar;