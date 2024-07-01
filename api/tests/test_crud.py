import pytest
import uuid

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from api.models import Base, Song
from api.crud import get_songs, search_songs, rate_song, get_song, create_song
from api.schemas import RatingCreate
from api.tests.utils_song_gen import create_random_song
from fastapi import status
from fastapi.exceptions import HTTPException

# from database import engine, SessionLocal


# @pytest.fixture(scope="module")
# def db_session():
#     Base.metadata.create_all(bind=engine)
#     session = SessionLocal()
#     yield session
#     session.close()
#     Base.metadata.drop_all(bind=engine)


# @pytest.fixture(scope="function")
# def sample_song(db_session):
#     song = Song(
#         id="1",
#         title="Test Song",
#         danceability=0.8,
#         energy=0.7,
#         key=5,
#         loudness=-5.0,
#         mode=1,
#         acousticness=0.1,
#         instrumentalness=0.0,
#         liveness=0.3,
#         valence=0.6,
#         tempo=120.0,
#         duration_ms=200000,
#         time_signature=4,
#         num_bars=100,
#         num_sections=5,
#         num_segments=10,
#         class_field=1,
#     )
#     db_session.add(song)
#     db_session.commit()
#     return song


def test_create_song(db_session):
    song_data = create_random_song()

    song = create_song(db_session, song=song_data)
    assert song.title == song_data.title
    assert song.danceability == song_data.danceability
    assert song.energy == song_data.energy
    assert song.key == song_data.key
    assert song.loudness == song_data.loudness
    assert song.mode == song_data.mode
    assert song.acousticness == song_data.acousticness
    assert song.instrumentalness == song_data.instrumentalness
    assert song.liveness == song_data.liveness
    assert song.valence == song_data.valence
    assert song.tempo == song_data.tempo
    assert song.duration_ms == song_data.duration_ms
    assert song.time_signature == song_data.time_signature
    assert song.num_bars == song_data.num_bars
    assert song.num_sections == song_data.num_sections
    assert song.num_segments == song_data.num_segments
    assert song.class_field == song_data.class_field


def test_get_songs(db_session):
    song_data = create_random_song()
    create_song(db_session, song=song_data)
    songs = get_songs(db_session, offset=0, limit=10)
    assert len(songs) >= 2


def test_search_songs(db_session):
    song_data = create_random_song()
    create_song(db_session, song=song_data)
    songs = search_songs(db_session, title=song_data.title)
    assert len(songs) == 1
    assert songs[0].title == song_data.title


def test_rate_song(db_session):
    song_data = create_random_song()
    create_song(db_session, song=song_data)
    rating = RatingCreate(rating=5.0)
    song = rate_song(db_session, song_id=song_data.id, rating=rating)
    assert song.rating == 5.0
    assert song.rating_count == 1


def test_get_song(db_session):
    song_data = create_random_song()
    create_song(db_session, song=song_data)
    song = get_song(db_session, song_id=song_data.id)
    assert song.title == song.title


def test_get_nonexistent_song(db_session):
    # song = get_song(db_session, song_id="99")
    # assert song is None
    with pytest.raises(HTTPException) as exc:
        get_song(db_session, song_id=str(uuid.uuid4()))
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "Song not found"


def test_search_nonexistent_song(db_session):
    songs = search_songs(db_session, title="Nonexistent")
    assert len(songs) == 0


def test_rate_song_multiple_times(db_session):
    song_data = create_random_song()
    create_song(db_session, song=song_data)
    rating1 = RatingCreate(rating=4.0)
    rating2 = RatingCreate(rating=5.0)
    song = rate_song(db_session, song_id=song_data.id, rating=rating1)
    song = rate_song(db_session, song_id=song_data.id, rating=rating2)
    assert song.rating == 4.5  # 5+4/2
    assert song.rating_count == 2  # 1+1
