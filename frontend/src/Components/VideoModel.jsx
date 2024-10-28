import React, { useRef, useState, useEffect } from 'react';
import video_before from "../dist/images/video-player.gif";
import video_loading from "../dist/images/loading.gif";
import video_after from "../dist/images/video.gif";

const VideoModal = ({ id }) => {
  const modalRef = useRef(null);
  const [videoState, setVideoState] = useState('before');
  const [videoUrl, setVideoUrl] = useState('');
  const [isPolling, setIsPolling] = useState(false);

  const openModal = async () => {
    modalRef.current.showModal();
    await getVideo();
  };

  const closeModal = () => {
    modalRef.current.close();
    setIsPolling(false);
  };

  const getVideo = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/check_video/${id}`);
      const data = await response.json();

      if (data.status === 'not_found') {
        // Send request to create video
        const createResponse = await fetch('http://127.0.0.1:8000/create_video', {
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
      console.error('Error fetching video:', error);
    }
  };

  useEffect(() => {
    let interval;
    if (isPolling) {
      interval = setInterval(async () => {
        try {
          const response = await fetch(`http://127.0.0.1:8000/check_video/${id}`);
          const data = await response.json();

          if (data.status === 'completed') {
            setVideoState('after');
            setVideoUrl(data.video_url);
            setIsPolling(false);
          }
        } catch (error) {
          console.error('Error polling:', error);
        }
      }, 1000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPolling, id]);

  return (
    <div>
      <img
        src={videoState === 'before' ? video_before : videoState === 'loading' ? video_loading : video_after}
        alt="Video State"
        className="cursor-pointer"
        onClick={openModal}
        style={{ width: '200px', height: 'auto' }}
      />
      <dialog ref={modalRef} className="modal">
        <div className="modal-box w-11/12 max-w-5xl">
          <h3 className="font-bold text-lg">Video Durumu</h3>
          <div className="py-4">
            {videoState === 'loading' && (
              <div className="flex items-center justify-center">
                <span className="loading loading-spinner loading-lg"></span>
              </div>
            )}
            {videoState === 'after' && videoUrl ? (
              <video controls autoPlay className="w-full" name="media">
                <source src={videoUrl} type="video/mp4" />
              </video>
            ) : (
              videoState !== 'loading' && <p>Video hazırlanıyor...</p>
            )}
          </div>
          <div className="modal-action">
            <button type="button" className="btn" onClick={closeModal}>Kapat</button>
          </div>
        </div>
      </dialog>
    </div>
  );
};

export default VideoModal;