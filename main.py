from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from book import *
from database import *

app = FastAPI



# app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = DBBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(DBBook).offset(skip).limit(limit).all()
    return books


@app.post("/reviews/", response_model=Review)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = DBReview(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/reviews/{book_id}", response_model=List[Review])
def get_reviews_for_book(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(DBReview).filter(DBReview.book_id == book_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="Book has no reviews")
    return reviews