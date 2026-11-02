from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0",
    description="Backend API for MallNav indoor navigation and store directory",
)

origins = [
    "http://localhost:3000",  # Standard React / Next.js dev server
    "http://127.0.0.1:3000",
]

# Add CORS middleware to the FastAPI pipeline
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies which domains, protocols, and ports can execute requests against this API
    allow_credentials=True,  # Enables support for cookies, authorization headers, or TLS client certificates across origins.
    allow_methods=["*"],  # Specifies allowed HTTP methods(GET, POST, PATCH, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allows headers like Content-Type, Authorization
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "environment": settings.APP_ENV}
