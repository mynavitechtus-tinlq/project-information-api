from pydantic import BaseModel


class BaseEntityModel(BaseModel):
    class Config:
        from_attributes = True
