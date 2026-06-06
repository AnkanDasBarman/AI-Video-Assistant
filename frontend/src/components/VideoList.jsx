import VideoCard from "./VideoCard";

function VideoList({ videos }) {
  return (
    <div className="video-grid">
      {videos.map((video) => (
        <VideoCard
          key={video.video_id}
          video={video}
        />
      ))}
    </div>
  );
}

export default VideoList;
