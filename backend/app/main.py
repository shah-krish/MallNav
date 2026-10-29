from app.api.v1.api import api_router
from fastapi import FastAPI

app = FastAPI(
    title = "MallNav API",
    version = "1.0",
    description= "Backend API for MallNav indoor navigation and store directory"
)

app.include_router(api_router, prefix='/api/v1')

@app.get("/health", tags=['health'])
def health_check():
    return {'status':'ok'}
