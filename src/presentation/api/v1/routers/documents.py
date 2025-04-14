from fastapi import APIRouter, status, UploadFile
from dishka.integrations.fastapi import FromDishka, DishkaRoute


documents_router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Resource for upload documents"],
    route_class=DishkaRoute
)


@documents_router.post(
    path="/upload-file",
    status_code=status.HTTP_201_CREATED,
    response_model=...
)
async def upload_file(file: UploadFile) -> ...:
    ...
