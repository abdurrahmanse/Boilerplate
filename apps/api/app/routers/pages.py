from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.database import get_db
from app.models import Page as PageModel
from app.schemas import Page

router = APIRouter(prefix="/pages", tags=["pages"])

@router.get("/", response_model=List[Page])
async def get_pages(q: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    stmt = select(PageModel)
    if q:
        stmt = stmt.filter(PageModel.name.contains(q))
    
    result = await db.execute(stmt)
    pages = result.scalars().all()
    return pages
