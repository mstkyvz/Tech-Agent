import React from 'react';
import video_ref from "../video.mp4" 

const MainPage = () => {
  return (
    <div className="flex flex-col justify-center items-center w-full h-full ">
        <div className="flex rounded-3xl shadow-xl justify-center items-center w-9/12 h-9/12 ">
        
      <video
                controls
                autoPlay
                className="w-full rounded-3xl shadow-xl"
                name="media"
              >
                <source src={video_ref} type="video/mp4" />
              </video>
    </div>
    </div>
  );
};

export default MainPage;