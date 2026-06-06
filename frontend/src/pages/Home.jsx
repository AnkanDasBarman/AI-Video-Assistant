import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api";

import UploadVideo from "../components/UploadVideo";
import UploadYoutube from "../components/UploadYoutube";
import VideoList from "../components/VideoList";

function Home() {
  const navigate = useNavigate();
  const [videos, setVideos] = useState([]);
  const [recentVideo, setRecentVideo] = useState(null);
  const totalFrames = videos.reduce(
    (total, video) => total + Number(video.frames || 0),
    0
  );
  const totalChunks = videos.reduce(
    (total, video) => total + Number(video.chunks || 0),
    0
  );

  const loadVideos = async () => {
    try {
      const res = await api.get("/videos");

      setVideos(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadVideos();
  }, []);

  useEffect(() => {
    console.log("Home: recentVideo updated =", recentVideo);
  }, [recentVideo]);

  return (
    <div className="home-page">
      <h1 className="hero-title">AI Video Assistant</h1>
      <p className="hero-subtitle">
        AI-powered multimodal video understanding platform
      </p>

      <div className="upload-section">
        <UploadVideo
          refreshVideos={loadVideos}
          onProcessed={setRecentVideo}
        />

        <UploadYoutube
          refreshVideos={loadVideos}
          onProcessed={setRecentVideo}
        />
      </div>

      {recentVideo && (
        <div className="recent-upload">
          <div className="recent-content">
            <div className="recent-badge">NEW</div>

            <h3>
              {recentVideo.title ||
                recentVideo.filename ||
                recentVideo.video_id}
            </h3>

            <p>
              Processing complete. Your video is ready for AI search.
            </p>
          </div>

          <button
            className="open-btn"
            onClick={() =>
              navigate(`/video/${recentVideo.video_id}`)
            }
          >
            Open Now →
          </button>
        </div>
      )}

      <div className="stats-bar">
        <div className="stat-card">
          <span>Videos</span>

          <strong>{videos.length}</strong>
        </div>

        <div className="stat-card">
          <span>Search Ready</span>

          <strong>100%</strong>
        </div>

        <div className="stat-card">
          <span>AI Index</span>

          <strong>Active</strong>
        </div>
      </div>

      <VideoList videos={videos} />
    </div>
  );
}

export default Home;
