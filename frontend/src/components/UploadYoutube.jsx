import { useState } from "react";
import api from "../api";

function UploadYoutube({ refreshVideos, onProcessed }) {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState("idle");
  const isBusy = status === "uploading" || status === "processing";

  const uploadVideo = async () => {
    try {
      console.log("UploadYoutube: Starting YouTube import for URL:", url);
      setStatus("processing");

      const res = await api.post("/upload-url", {
        url,
      });

      console.log("UploadYoutube: Response received:", res.data);
      setStatus("done");
      setUrl("");

      const processedVideo = {
        title: res.data.title || "YouTube video",
        ...res.data,
      };

      console.log("UploadYoutube: Setting processed video:", processedVideo);
      onProcessed(processedVideo);

      await refreshVideos();
    } catch (err) {
      console.error("UploadYoutube: Import failed:", err);

      setStatus("idle");

      alert("Upload failed");
    }
  };

  return (
    <div className="upload-card">
      <div className="upload-card-header">
        <span className="upload-icon">Link</span>

        <h2>Import from YouTube</h2>
      </div>

      <p className="upload-copy">
        Paste a YouTube URL to download and process it for multimodal search.
      </p>

      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Paste YouTube URL"
      />

      <button
        onClick={uploadVideo}
        disabled={isBusy || !url}
      >
        {isBusy ? "Processing..." : "Import Video"}
      </button>

      {isBusy && (
        <div className="upload-progress">
          <div className="loader"></div>

          <div className="processing-steps">
            <span className="step done">URL Received</span>

            <span className="step active">Processing Video</span>

            <span className="step">Building AI Indexes</span>
          </div>

          <div className="progress-track">
            <div
              className="progress-fill"
              style={{
                width: "65%",
              }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UploadYoutube;
