from fastapi import FastAPI, HTTPException, Depends, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List
from api.database import SessionLocal
from api.schemas import SongCreate, SongResponse, RatingCreate, PaginatedResponse
from contextlib import asynccontextmanager
import api.crud as crud
from typing import Annotated


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     init_db()
#     yield


# app = FastAPI(lifespan=lifespan)
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


@app.get("/songs/", response_model=PaginatedResponse[SongResponse])
def get_songs(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_songs(db, page=page, limit=limit)


@app.post("/songs/", response_model=SongResponse)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    return crud.create_song(db, song=song)


@app.get("/songs/search/", response_model=List[SongResponse])
def search_songs(
    title: Annotated[str, Query(..., min_length=1, max_length=100)],
    db: Session = Depends(get_db),
):
    return crud.search_songs(db, title=title)


@app.post("/songs/{song_id}/rate/", response_model=SongResponse)
def rate_song(
    song_id: Annotated[str, Path(..., min_length=1, max_length=50)],
    rating: RatingCreate,
    db: Session = Depends(get_db),
):
    if not 0 <= rating.rating <= 5:
        raise HTTPException(
            status_code=400, detail="Invalid rating. Must be between 0 and 5."
        )
    return crud.rate_song(db, song_id=song_id, rating=rating)


@app.get("/songs/{song_id}/", response_model=SongResponse)
def get_song(
    song_id: Annotated[str, Path(..., min_length=1, max_length=50)],
    db: Session = Depends(get_db),
):
    return crud.get_song(db, song_id=song_id)
