import React, { useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';

function VideoPlayer() {
  const { videoId } = useParams();
  const videoRef = useRef(null);
  const peerConnectionRef = useRef(null);

  useEffect(() => {
    const initWebRTC = async () => {
      const configuration = { iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };
      peerConnectionRef.current = new RTCPeerConnection(configuration);

      // Set up signaling (simplified for this example)
      const socket = new WebSocket('ws://localhost:3000');

      socket.onmessage = async (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'offer') {
          await peerConnectionRef.current.setRemoteDescription(new RTCSessionDescription(message));
          const answer = await peerConnectionRef.current.createAnswer();
          await peerConnectionRef.current.setLocalDescription(answer);
          socket.send(JSON.stringify(answer));
        }
      };

      peerConnectionRef.current.ontrack = (event) => {
        if (videoRef.current) {
          videoRef.current.srcObject = event.streams[0];
        }
      };

      // Request the video stream
      socket.send(JSON.stringify({ type: 'request_stream', videoId }));
    };

    initWebRTC();

    return () => {
      if (peerConnectionRef.current) {
        peerConnectionRef.current.close();
      }
    };
  }, [videoId]);

  return <video ref={videoRef} autoPlay controls />;
}

export default VideoPlayer;
