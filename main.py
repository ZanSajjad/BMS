
from fastapi import FastAPI, Request, Form, File, Depends,UploadFile,HTTPException
from  fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
import shutil
from typing import Optional
from database import *
from models import *

app = FastAPI()


UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#add the css or static path
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")

templates = Jinja2Templates(directory="templates")


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

# bind engine from database call
init_db()

# homepage
@app.get("/")
async def root(request: Request,db: Session=Depends(get_db)):
    books = db.query(Book).all()
    return  templates.TemplateResponse("index.html", {"request": request,"books":books})

# upload page
@app.get("/upload")
async def upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
    
# upload data to the database   
@app.post("/upload")
async def upload_book(request:Request, image: UploadFile = File(...),
                 title: str = Form(...),genre:str = Form(...),
                 author:str = Form(...), price: float = Form(...),
                 year:int    = Form(...),db: Session=Depends(get_db)):

    # Ensure the uploaded file has a unique name
    file_location = f"{UPLOAD_DIR}/{image.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    book = Book(title=title,genre=genre,author=author,price=price,year=year,cover_img=file_location)
    db.add(book)
    db.commit()
    db.refresh(book)
    return RedirectResponse (url="/",status_code=303)

# redirect to the book 
@app.get("/update/{book_id}")
def update_book_form(book_id:int,request: Request,db: Session=Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return templates.TemplateResponse("update.html", {"request": request,"book":book})

# update the book 
@app.post("/update/{book_id}")
async def update_book(book_id: int, title: str = Form(...), genre: str = Form(...),
                      author: str = Form(...), price: float = Form(...),
                      year: int = Form(...), image: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = title
    book.genre = genre
    book.author = author
    book.price = price
    book.year = year

    if image and image.filename:
        file_location = f"{UPLOAD_DIR}/{image.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        book.cover_img = file_location

    db.commit()
    return RedirectResponse(url="/", status_code=303)
    
    
# delete the book id
@app.get("/delete/{book_id}")
def delete_book(book_id:int,db: Session=Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.cover_img and os.path.exists(book.cover_img):
        os.remove(book.cover_img)
    db.delete(book)
    db.commit()
    return RedirectResponse (url="/",status_code=303)
