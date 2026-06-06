class VideoService:
    def ingest_video(self, path: str):
        return {
            "path": path,
            "status": "video ingestion placeholder"
        }

    def extract_frames(self, path: str):
        return {
            "path": path,
            "status": "frame extraction placeholder"
        }
