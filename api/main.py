from fastapi import FastAPI, File, HTTPException, Depends, Query, Path, Body, UploadFile
from sqlalchemy.orm import Session
from typing import List
from api.database import SessionLocal
from api.schemas import (
    SongCreate,
    SongResponse,
    RatingCreate,
    PaginatedResponse,
    InsertionResult,
)
from contextlib import asynccontextmanager
import api.crud as crud
from typing import Annotated


app = FastAPI()


def get_db():
    """
    Dependency function to get a database session.

    Returns:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # close the database connection


@app.get("/")
def read_root():
    """
    Root endpoint to test the API.

    Returns:
        dict: A simple greeting message.
    """
    return {"Hello": "World"}


@app.get("/songs/", response_model=PaginatedResponse[SongResponse])
def get_songs(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(
        default=20, ge=1, le=100, description="Number of items per page"
    ),
    db: Session = Depends(get_db),
):
    """
    Get a paginated list of songs.

    - **page**: Page number (default: 1)
    - **limit**: Number of items per page (default: 20, max: 100)

    Returns a paginated response containing the songs.
    """
    return crud.get_songs(db, page=page, limit=limit)


@app.post("/songs/", response_model=SongResponse)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    """
    Create a new song.

     - **song**: Song data

     Returns the created song.
    """
    return crud.create_song(db, song=song)


@app.get("/songs/search/", response_model=List[SongResponse])
def search_songs(
    title: Annotated[
        str, Query(..., min_length=1, max_length=100, description="Title to search for")
    ],
    db: Session = Depends(get_db),
):
    """
    Search songs by title.

    - **title**: Title to search for (min length: 1, max length: 100)

    Returns a list of songs matching the search criteria.
    """
    return crud.search_songs(db, title=title)


@app.post("/songs/{song_id}/rate/", response_model=SongResponse)
def rate_song(
    song_id: Annotated[
        str,
        Path(..., min_length=1, max_length=50, description="ID of the song to rate"),
    ],
    rating: RatingCreate,
    db: Session = Depends(get_db),
):
    """
    Rate a song.

    - **song_id**: ID of the song to rate
    - **rating**: Rating data

    Returns the updated song with the new rating.

    Raises:
    - HTTPException (400): If the rating is invalid (not between 0 and 5).

    """
    if not 0 <= rating.rating <= 5:
        raise HTTPException(
            status_code=400, detail="Invalid rating. Must be between 0 and 5."
        )
    return crud.rate_song(db, song_id=song_id, rating=rating)


@app.get("/songs/{song_id}/", response_model=SongResponse)
def get_song(
    song_id: Annotated[
        str,
        Path(
            ..., min_length=1, max_length=50, description="ID of the song to retrieve"
        ),
    ],
    db: Session = Depends(get_db),
):
    """
    Get a song by ID.

    - **song_id**: ID of the song to retrieve

    Returns the requested song.
    """
    return crud.get_song(db, song_id=song_id)


@app.post("/upload", response_model=InsertionResult)
def upload_songs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a playlist file.

    - **file**: The playlist file to upload

    Returns the result of the playlist file upload.
    """
    return crud.upload_playlist_file(db, file.file)
