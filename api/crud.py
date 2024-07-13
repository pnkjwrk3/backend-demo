from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models import Song
from api.schemas import (
    SongCreate,
    SongResponse,
    RatingCreate,
    PaginatedResponse,
    InsertionResult,
)
from typing import List
from api.utils import normalize_json_to_dicts
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError


def get_songs(
    db: Session,
    page: int = 0,
    limit: int = 20,
) -> PaginatedResponse[SongResponse]:
    total_items = db.query(func.count(Song.id)).scalar()
    total_pages = (total_items + limit - 1) // limit
    offset = (page - 1) * limit
    songs = db.query(Song).offset(offset).limit(limit).all()

    next_page = f"/songs/?page={page + 1}&limit={limit}" if page < total_pages else None
    prev_page = f"/songs/?page={page - 1}&limit={limit}" if page > 1 else None

    return PaginatedResponse[SongResponse](
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        items_per_page=limit,
        next_page=next_page,
        prev_page=prev_page,
        data=[SongResponse.model_validate(song) for song in songs],
    )


def create_song(db: Session, song: SongCreate) -> SongResponse:
    """
    Create a new song entry in the database.
    """
    db_song = Song(**song.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return SongResponse.model_validate(db_song)


# Limit the number of songs to be returned to 10
def search_songs(db: Session, title: str) -> List[SongResponse]:
    """
    Search for songs by title. Limits the result to 10 songs.
    """
    songs = db.query(Song).filter(Song.title.ilike(f"%{title}%")).limit(10).all()
    return [SongResponse.model_validate(song) for song in songs]


def rate_song(
    db: Session,
    song_id: str,
    rating: RatingCreate,
) -> SongResponse:
    """
    Rate a song with a rating value between 0 and 5.
    """
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    song.rating = round(
        (song.rating * song.rating_count + rating.rating) / (song.rating_count + 1), 2
    )
    song.rating_count += 1

    db.commit()
    db.refresh(song)
    return SongResponse.model_validate(song)


def get_song(db: Session, song_id: str) -> SongResponse:
    """
    Retrieve a specific song by its ID.
    """
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return SongResponse.model_validate(song)


def upload_playlist_file(db: Session, input_file) -> dict:
    records = normalize_json_to_dicts(input_file)
    return insert_records(db, records)


def insert_records(db: Session, records: List[dict]) -> dict:
    duplicates = []
    inserted = 0

    for record in records:
        try:
            # Validate the record
            song = SongCreate(**record)

            # Insert the record into the database
            create_song(db, song=song)
            inserted += 1
        except IntegrityError:
            # Handle duplicate keys
            duplicates.append(record["id"])
            db.rollback()
        except ValidationError as e:
            # Handle validation errors
            print(f"Validation error: {e}")
            continue

    return InsertionResult(inserted=inserted, errors=duplicates)
