from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, TypeVar, Generic


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


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    total_items: int
    total_pages: int
    current_page: int
    items_per_page: int
    next_page: Optional[str]
    prev_page: Optional[str]
    data: List[T]
