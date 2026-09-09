from pydantic import BaseModel

class PageBase(BaseModel):
    name: str

class PageCreate(PageBase):
    pass

class Page(PageBase):
    id: int

    model_config = {"from_attributes": True}
