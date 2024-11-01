import React from 'react';
import { MessageSquare, Settings, Book, PenTool, MessageCircle, X } from 'lucide-react';
import config from '../config.json'; 

const Sidebar = ({ isOpen, chatHistories = [], onHistorySelect }) => {
  const handleDelete = async (historyId, event) => {
    event.stopPropagation(); 
    try {
      const response = await fetch(`${config.apiUrl}/delete_chat_history/${historyId}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        if (onHistorySelect) {
          onHistorySelect(null);
        }
      }
    } catch (error) {
      console.error('Error deleting chat history:', error);
    }
  };

  return (
    <div className="relative">
      <aside className={`${isOpen ? 'w-56' : 'w-0'} h-full bg-white transition-all duration-300 ease-in-out overflow-hidden`}>
        <ul className="menu w-56 flex flex-col h-full py-4">
          <li>
            <a href="/konu" className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
              <Book size={18} />
              Konu Anlatım
            </a>
          </li>
          <li>
            <a href="/soru" className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
              <PenTool size={18} />
              Soru Çöz
            </a>
          </li>
          <li>
            <a href="/soruolustur" className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
              <MessageSquare size={18} />
              Soru Oluştur
            </a>
          </li>
          <li>
            <a href="/podcast" className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
              <MessageCircle size={18} />
              Tartışma
            </a>
          </li>
          
          {chatHistories.length > 0 && (
            <li className="mt-4">
              <span className="text-sm text-gray-500 px-4 py-2 block">
                Chat History
              </span>
              <ul className="mt-2 max-h-96 overflow-y-auto">
                {chatHistories.map((history) => (
                  <li key={history.id} className="relative group">
                    <button
                      onClick={() => onHistorySelect(history.id)}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100 text-sm pr-8"
                    >
                      Chat-{history.title}
                    </button>
                    <button
                      onClick={(e) => handleDelete(history.id, e)}
                      className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 hover:text-red-500 transition-opacity p-1"
                      aria-label="Delete chat history"
                    >
                      <X size={16} />
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