from pydantic import BaseModel, Field
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler, BaseCacheable, CacheType
from app.db.fake_db import fake_todo_db


class GetTodoByIdDataRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, description="The item id be greater than zero")


class GetTodoByIdDataResponse(BaseModel, BaseResponse):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoByIdDataHandler(BaseHandler):

    async def handle(self, req: GetTodoByIdDataRequest) -> GetTodoByIdDataResponse:
        for it in fake_todo_db:
            if it["id"] == req.id:
                return GetTodoByIdDataResponse(id=it["id"], title=it["title"])

        return None
