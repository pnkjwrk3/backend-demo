import pytest
import uuid
from fastapi.testclient import TestClient

# from sqlalchemy.orm import sessionmaker
from api.main import app, get_db
from api.models import Base, Song
from api.schemas import SongCreate

from api.database import engine, SessionLocal

from api.tests.utils_song_gen import create_random_song, create_random_song_dict
from fastapi import status
from fastapi.exceptions import HTTPException


# def override_get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)


# @pytest.fixture(scope="module", autouse=True)
# def setup_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


# @pytest.fixture(scope="function")
# def db_session():
#     session = SessionLocal()
#     yield session
#     session.close()


@pytest.fixture(scope="function")
def sample_song(db_session):
    song = Song(
        id="1",
        title="Test Song",
        danceability=0.8,
        energy=0.7,
        key=5,
        loudness=-5.0,
        mode=1,
        acousticness=0.1,
        instrumentalness=0.0,
        liveness=0.3,
        valence=0.6,
        tempo=120.0,
        duration_ms=200000,
        time_signature=4,
        num_bars=100,
        num_sections=5,
        num_segments=10,
        class_field=1,
    )
    db_session.add(song)
    db_session.commit()
    return song


def test_create_song(client):
    song_data = create_random_song_dict()
    response = client.post("/songs/", json=song_data)
    assert response.status_code == 200
    content = response.json()
    # print(content["title"])
    assert content["title"] == song_data["title"]
    assert content["danceability"] == song_data["danceability"]
    assert content["duration_ms"] == song_data["duration_ms"]
    assert content["class_field"] == song_data["class"]


def test_get_songs(client):
    song_data1 = create_random_song_dict()
    song_data2 = create_random_song_dict()
    client.post("/songs/", json=song_data1)
    client.post("/songs/", json=song_data2)
    response = client.get("/songs/")
    assert response.status_code == 200
    songs = response.json()
    assert len(songs) >= 2
    # assert songs[0]["title"] == "Test Song"


def test_search_songs(client):
    song_data = create_random_song_dict()
    client.post("/songs/", json=song_data)
    response = client.get(f"/songs/search/?title={song_data['title']}")
    assert response.status_code == 200
    songs = response.json()
    assert len(songs) == 1
    assert songs[0]["title"] == song_data["title"]


def test_rate_song(client):
    song_data = create_random_song_dict()
    client.post("/songs/", json=song_data)
    song_id = str(song_data.get("id"))
    response = client.post(f"/songs/{song_id}/rate/", json={"rating": 5.0})
    assert response.status_code == 200
    song = response.json()
    assert song["rating"] == 5.0
    assert song["rating_count"] == 1


def test_get_song(client):
    song_data = create_random_song_dict()
    client.post("/songs/", json=song_data)
    song_id = str(song_data.get("id"))
    response = client.get(f"/songs/{song_id}/")
    assert response.status_code == 200
    song = response.json()
    assert song["title"] == song_data["title"]


def test_get_nonexistent_song(client):
    response = client.get(f"/songs/{str(uuid.uuid4())}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Song not found"


def test_rate_nonexistent_song(client):
    response = client.post(f"/songs/{str(uuid.uuid4())}/rate/", json={"rating": 5.0})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Song not found"


def test_search_nonexistent_song(client):
    response = client.get("/songs/search/?title=Nonexistent")
    assert response.status_code == 200
    songs = response.json()
    assert len(songs) == 0
