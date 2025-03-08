from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    price: float
    cover_img: str


class Book(BookCreate):
    id: int

    class Config:
        orm_mode = True
