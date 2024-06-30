from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from api.models import Song
from api.schemas import SongCreate, SongResponse, RatingCreate


def get_songs(db: Session, offset: int = 0, limit: int = 10):
    return db.query(Song).offset(offset).limit(limit).all()


def create_song(db: Session, song: SongCreate):
    db_song = Song(**song.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


def search_songs(db: Session, title: str):
    return db.query(Song).filter(Song.title.ilike(f"%{title}%")).all()


def rate_song(db: Session, song_id: str, rating: RatingCreate):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    song.rating = (song.rating * song.rating_count + rating.rating) / (
        song.rating_count + 1
    )
    song.rating_count += 1

    db.commit()
    db.refresh(song)
    return song


def get_song(db: Session, song_id: str):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song
