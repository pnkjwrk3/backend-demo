from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from api.database import SessionLocal, engine
from api.models import Base, Song
from api.schemas import SongCreate, SongResponse, RatingCreate
import api.crud as crud

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # close the database connection


# API Endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/songs/", response_model=List[SongResponse])
def get_songs(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_songs(db, offset=offset, limit=limit)


@app.post("/songs/", response_model=SongResponse)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    return crud.create_song(db, song=song)


@app.get("/songs/search/", response_model=List[SongResponse])
def search_songs(title: str, db: Session = Depends(get_db)):
    return crud.search_songs(db, title=title)


@app.post("/songs/{song_id}/rate/", response_model=SongResponse)
def rate_song(song_id: str, rating: RatingCreate, db: Session = Depends(get_db)):
    return crud.rate_song(db, song_id=song_id, rating=rating)


@app.get("/songs/{song_id}/", response_model=SongResponse)
def get_song(song_id: str, db: Session = Depends(get_db)):
    return crud.get_song(db, song_id=song_id)
