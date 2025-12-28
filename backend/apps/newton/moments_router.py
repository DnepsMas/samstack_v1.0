from fastapi import APIRouter, Query

from . import moments_crud

router = APIRouter()


@router.get("/moments")
async def list_moments(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    moments = moments_crud.list_moments(limit=limit, offset=offset)
    return {"success": True, "moments": moments}
