from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.database.session import get_session
from app.schemas.parse import ParseData
from app.services.parser import parse_and_store

router = APIRouter(prefix="/parse", tags=["parser"])


@router.post("/")
async def parse_endpoint(session: AsyncSession = Depends(get_session)) -> ParseData:
    created_count = await parse_and_store(session)
    return {"created": created_count}
