# AI Video Assistant

A multimodal video understanding system that enables semantic search, question answering, timeline generation, highlights extraction, and visual search over uploaded videos.

## Features

- Video Upload
- YouTube Import
- Whisper Transcription
- Semantic Transcript Search
- Question Answering (RAG)
- Timeline Generation
- AI Highlights
- Visual Search using BLIP
- FastAPI Backend
- React Frontend

## Tech Stack

### Backend
- FastAPI
- Whisper
- FAISS
- Sentence Transformers
- BLIP
- OpenAI

### Frontend
- React
- Axios
- Framer Motion
- React Router

## Run Backend

```bash
cd multimodal-qa-agent
venv\Scripts\activate      # Windows
# source venv/bin/activate # Mac/Linux
uvicorn api.app:app --reload
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

## Future Improvements

- OCR Search
- Clip Extraction
- Cross Video Search
- Object Detection
- Video Chapters
