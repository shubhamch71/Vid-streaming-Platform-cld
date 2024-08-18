import React, { useState } from 'react';
import axios from 'axios';

function VideoUpload() {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('video', file);
    formData.append('title', title);

    try {
      const response = await axios.post('/api/videos/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      console.log(response.data);
      // Handle successful upload (e.g., show success message, redirect)
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Video Title"
        required
      />
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        accept="video/*"
        required
      />
      <button type="submit">Upload Video</button>
    </form>
  );
}

export default VideoUpload;
