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
<img width="1896" height="968" alt="image" src="https://github.com/user-attachments/assets/bee950ee-f0b5-4c3a-8c2c-7c097008deea" />
<img width="1806" height="878" alt="image" src="https://github.com/user-attachments/assets/e00754ec-30ae-446a-aa47-3b408e36c984" />
<img width="1918" height="1023" alt="image" src="https://github.com/user-attachments/assets/f9879667-0c10-4ba1-a3c7-42eecabe0379" />
<img width="1393" height="904" alt="image" src="https://github.com/user-attachments/assets/b2693fa4-8243-4407-9e06-fafea9e16b71" />
<img width="1201" height="745" alt="image" src="https://github.com/user-attachments/assets/2af37227-de8a-4018-8c4f-173b401a6a5a" />
<img width="1046" height="252" alt="image" src="https://github.com/user-attachments/assets/e705a03f-0eda-4bc7-a695-c47242b576d8" />

