from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import routers
from .routes import timeline, video_search, visual_search, video_highlights, video_stream

app = FastAPI(title="Multimodal QA Agent")

# Serve uploaded video files via static route
app.mount("/uploads", StaticFiles(directory="backend/uploads"), name="uploads")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Multimodal QA Agent API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Include routers
app.include_router(
    timeline.router,
    prefix="/video-timeline",
    tags=["timeline"],
)

app.include_router(
    video_search.router,
    tags=["video_search"],
)

app.include_router(
    visual_search.router,
    tags=["visual_search"],
)

app.include_router(
    video_highlights.router,
    tags=["video_highlights"],
)

app.include_router(
    video_stream.router,
    tags=["video_stream"],
)
