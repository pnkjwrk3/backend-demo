from pydantic import BaseModel, Field, ConfigDict


class SongCreate(BaseModel):
    id: str
    title: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
    num_bars: int
    num_sections: int
    num_segments: int
    class_field: int = Field(alias="class")


class SongResponse(SongCreate):
    id: str
    title: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
    num_bars: int
    num_sections: int
    num_segments: int
    class_field: int = Field(alias="class")
    rating: float
    rating_count: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    # class config:
    #     from_attributes = True
    #     populate_by_name = True


class RatingCreate(BaseModel):
    rating: float
