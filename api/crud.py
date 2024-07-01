from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from api.models import Song
from api.schemas import SongCreate, SongResponse, RatingCreate


def get_songs(db: Session, offset: int = 0, limit: int = 10):
    songs = db.query(Song).offset(offset).limit(limit).all()
    return [SongResponse.model_validate(song) for song in songs]


def create_song(db: Session, song: SongCreate):
    db_song = Song(**song.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


# Limit the number of songs to be returned to 10
def search_songs(db: Session, title: str):
    songs = db.query(Song).filter(Song.title.ilike(f"%{title}%")).limit(10).all()
    return [SongResponse.model_validate(song) for song in songs]


def rate_song(db: Session, song_id: str, rating: RatingCreate):
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


def get_song(db: Session, song_id: str):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return SongResponse.model_validate(song)
