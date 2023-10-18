from sqlalchemy import create_engine, Column, Integer, String, create_engine, func, ForeignKey, TIMESTAMP
from database import Base, SessionLocal

class User(Base):
    __tablename__ = 'user'
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group = Column(Integer)
    gender = Column(Integer)
    id = Column(Integer, primary_key=True)
    os = Column(String)
    source = Column(String)

if __name__ == "__main__":
    session = SessionLocal()
    list_id = []
    for user in (
        session.query(User.country, User.os, func.count())
        .where(User.exp_group == 3)
        .group_by(User.country, User.os)
        .having(func.count()>100)
        .order_by(-func.count())
        ):
        list_id.append(user)
    print(list_id)