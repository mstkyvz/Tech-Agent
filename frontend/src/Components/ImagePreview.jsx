import React from 'react';

const ImagePreview = ({ selectedImageRender }) => {
  return (
    <div className="flex items-center shadow-2xl justify-center border-dashed rounded-lg border-[3px] border-green-400">
      {selectedImageRender && (
        <img
          src={selectedImageRender}
          alt="Selected"
          className="max-h-48 max-w-full object-contain"
        />
      )}
    </div>
  );
};

export default ImagePreview;