from fastapi import APIRouter
from app.api.v1.endpoints import stores

api_router = APIRouter()
# If stores.py defines @router.get("/"), adding prefix="/stores" turns that path into /stores
# Tags is used to group endpoints under Swagger docs UI
# stores.router = router object defined under stores. It tells FastAPI to include all the routes registered on stores.router
api_router.include_router(stores.router, prefix='/stores', tags=['stores'])