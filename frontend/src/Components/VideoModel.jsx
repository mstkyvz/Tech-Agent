import React, { useRef, useState, useEffect } from 'react';
import video_before from "../dist/images/video-player.gif";
import video_loading from "../dist/images/loading.gif";
import video_after from "../dist/images/video.gif";
import config from '../config.json'; 

const VideoModal = ({ id, saveChatHistory }) => {
  const modalRef = useRef(null);
  const videoRef = useRef(null);
  const [videoState, setVideoState] = useState('before');
  const [videoUrl, setVideoUrl] = useState('');
  const [isPolling, setIsPolling] = useState(false);

  const openModal = async () => {
    modalRef.current.showModal();
    await getVideo();
  };

  const closeModal = () => {
    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    }
    modalRef.current.close();
    setIsPolling(false);
  };

  const getVideo = async () => {
    try {
      saveChatHistory();
      const response = await fetch(`${config.apiUrl}/check_video/${id}`);
      const data = await response.json();

      if (data.status === 'not_found') {
        const createResponse = await fetch(`${config.apiUrl}/create_video`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id }),
        });

        if (createResponse.ok) {
          setVideoState('loading');
          setIsPolling(true);
        }
      } else if (data.status === 'completed') {
        setVideoState('after');
        setVideoUrl(data.video_url);
      }
    } catch (error) {
      console.error('Video yüklenirken hata oluştu:', error);
    }
  };

  useEffect(() => {
    let interval;
    if (isPolling) {
      interval = setInterval(async () => {
        try {
          const response = await fetch(`${config.apiUrl}/check_video/${id}`);
          const data = await response.json();

          if (data.status === 'completed') {
            setVideoState('after');
            setVideoUrl(data.video_url);
            setIsPolling(false);
          }
        } catch (error) {
          console.error('Kontrol sırasında hata:', error);
        }
      }, 1000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPolling, id]);

  // Handle modal close when ESC key is pressed
  useEffect(() => {
    const handleEscapeKey = (event) => {
      if (event.key === 'Escape') {
        closeModal();
      }
    };

    document.addEventListener('keydown', handleEscapeKey);
    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, []);

  return (
    <div>
      <img
        src={videoState === 'before' ? video_before : videoState === 'loading' ? video_loading : video_after}
        alt="Video Durumu"
        className="cursor-pointer hover:opacity-80 transition-opacity"
        onClick={openModal}
        style={{ width: '200px', height: 'auto' }}
      />
      <dialog
        ref={modalRef}
        className="modal"
        onClose={closeModal}
      >
        <div className="modal-box w-11/12 max-w-5xl">
          <h3 className="font-bold text-lg">Video Durumu</h3>
          <div className="py-4">
            {videoState === 'loading' && (
              <div className="flex items-center justify-center">
                <span className="loading loading-spinner loading-lg"></span>
              </div>
            )}
            {videoState === 'after' && videoUrl ? (
              <video
                ref={videoRef}
                controls
                className="w-full"
                name="media"
              >
                <source src={videoUrl} type="video/mp4" />
                Tarayıcınız video oynatmayı desteklemiyor.
              </video>
            ) : (
              videoState !== 'loading' && <p>Video hazırlanıyor...</p>
            )}
          </div>
          <div className="modal-action">
            <button 
              type="button" 
              className="btn hover:bg-gray-200"
              onClick={closeModal}
            >
              Kapat
            </button>
          </div>
        </div>
      </dialog>
    </div>
  );
};

export default VideoModal;
