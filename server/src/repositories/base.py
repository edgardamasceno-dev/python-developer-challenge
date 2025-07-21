from typing import Generic, TypeVar, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model
    
    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        return await self.session.get(self.model, id)
    
    async def count(self, *filters) -> int:
        query = select(func.count()).select_from(self.model)
        for f in filters:
            query = query.where(f)
        return await self.session.scalar(query)
    
    async def exists(self, **kwargs) -> bool:
        query = select(self.model).filter_by(**kwargs).limit(1)
        result = await self.session.execute(query)
        return result.scalar() is not None