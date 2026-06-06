from services.ingestion_service import ingest

video_path = ingest(
    "https://youtu.be/9UIadjn5Kuk?si=icP2pWYXIgRIXle9"
)
print(video_path)
