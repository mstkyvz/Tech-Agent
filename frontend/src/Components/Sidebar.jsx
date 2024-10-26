import React from 'react';
const Sidebar = ({ isOpen }) => {
    return (
        <div className="relative">
            <aside className={`${isOpen ? 'w-56' : 'w-0'} h-full bg-base-100`}>
                <ul className={`menu w-56 shadow-lg flex flex-col 
                      ${isOpen ? 'w-56 translate-x-0' : 'w-0 -translate-x-full'} 
                      h-full transition-transform duration-250 ease-in-out 
                      transform top-0 left-0 shadow-cr font-bold `}>

                    <li><a href='/konu'>Konu Anlatım</a></li>
                    <li><a href='/soru'>Soru Çöz</a></li>
                    <li><a href='/sorucoz'>Soru Oluştur</a></li>
                    <li><a href='/podcast'>Tartışma</a></li>
                    <li className="mt-auto"><a>Ayarlar</a></li>
                </ul>
            </aside>
        </div>
    );
};

export default Sidebar;
