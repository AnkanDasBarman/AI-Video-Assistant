import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

function VideoCard({ video }) {
  const navigate = useNavigate();

  return (
    <motion.div
      className="video-card"
      initial={{
        opacity: 0,
        y: 20,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      whileHover={{
        y: -8,
      }}
    >
      <h3>{video.title}</h3>

      

      <button
        className="open-btn"
        onClick={() =>
          navigate(
            `/video/${video.video_id}`
          )
        }
      >
        Open
      </button>
    </motion.div>
  );
}

export default VideoCard;
