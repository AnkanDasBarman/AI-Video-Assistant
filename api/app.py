from backend.api.app import app
from api.routes.upload import router as upload_router
from api.routes.process import router as process_router
from api.routes.qa import (
    router as qa_router
)
from api.routes.youtube import (
    router as youtube_router
)
from api.routes.videos import (
    router as videos_router
)

app.include_router(
    upload_router
)

app.include_router(
    process_router
)

app.include_router(
    qa_router
)

app.include_router(
    youtube_router
)

app.include_router(
    videos_router
)
