from sqlalchemy import create_engine, Column, Integer, String, create_engine, func, ForeignKey, TIMESTAMP
from database import Base, SessionLocal


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)


if __name__ == "__main__":
    session = SessionLocal()
    list_id = []
    for post in (session.query(Post).filter(Post.topic == 'business').order_by(-Post.id).limit(10)):
        list_id.append(post.id)
    print(list_id)    

