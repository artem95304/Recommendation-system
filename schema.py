from datetime import datetime
from pydantic import BaseModel

class UserGet(BaseModel):
    age: int
    city: str
    country: str
    exp_group: int
    gender: int
    id: int
    os: str
    source: str
    class Config:
        orm_mode = True 


class PostGet(BaseModel):
    id: int
    text: str
    topic: str
    class Config:
        orm_mode = True 


class FeedGet(BaseModel):
    user_id: int
    post_id: int
    user: UserGet
    post: PostGet
    action: str
    time: datetime
    class Config:
        orm_mode = True 