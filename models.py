from  sqlalchemy import Column, Integer, String ,Float
from  database import Base


class Book(Base):
    __tablename__ = "books"

    id =  Column(Integer, primary_key=True)
    title = Column(String,index=True)
    author = Column(String,index=True)
    price = Column(Float,index=True)
    year = Column(Integer,index=True)
    genre = Column(String,index=True)
    cover_img = Column(String , nullable=True)
