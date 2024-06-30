from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Model for songs table.
class Song(Base):
    __tablename__ = "songs"
    __table_args__ = {"schema": "playlist"}

    id = Column(String, primary_key=True)
    title = Column(String, index=True)
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    duration_ms = Column(Integer)
    time_signature = Column(Integer)
    num_bars = Column(Integer)
    num_sections = Column(Integer)
    num_segments = Column(Integer)
    class_field = Column(Integer, key="class", name="class")
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
