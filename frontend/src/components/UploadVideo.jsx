import { useState } from "react";
import api from "../api";

function UploadVideo({ refreshVideos, onProcessed }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle");
  const [progress, setProgress] = useState(0);
  const isBusy = status === "uploading" || status === "processing";

  const uploadFile = async () => {
    if (!file) return;

    setStatus("uploading");
    setProgress(0);

    const formData = new FormData();

    formData.append("file", file);

    try {
      const res = await api.post("/upload-video", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (event) => {
          if (!event.total) return;

          const percent = Math.round(
            (event.loaded * 100) / event.total
          );

          setProgress(percent);

          if (percent >= 100) {
            setStatus("processing");
          }
        },
      });

      setStatus("done");

      onProcessed({
        filename: file.name,
        ...res.data,
      });

      await refreshVideos();
    } catch (err) {
      console.error(err);

      setStatus("idle");

      alert("Upload failed");
    }
  };

  return (
    <div className="upload-card">
      <div className="upload-card-header">
        <span className="upload-icon">Video</span>

        <h2>Upload Video</h2>
      </div>

      <p className="upload-copy">
        Choose a local video and let the system process transcript, frames, and visual index.
      </p>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={uploadFile}
        disabled={isBusy || !file}
      >
        {status === "uploading" && "Uploading..."}
        {status === "processing" && "Processing..."}
        {(status === "idle" || status === "done") && "Upload"}
      </button>

      {isBusy && (
        <div className="upload-progress">
          <div className="loader"></div>

          <div className="processing-steps">
            <span className="step done">Upload Complete</span>

            <span className={status === "processing" ? "step active" : "step"}>
              Processing Video
            </span>

            <span className="step">Building AI Indexes</span>
          </div>

          <div className="progress-track">
            <div
              className="progress-fill"
              style={{
                width: `${status === "processing" ? 65 : progress}%`,
              }}
            ></div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UploadVideo;
