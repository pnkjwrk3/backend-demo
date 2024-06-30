set search_path = playlist;

-- Drop if exists
drop table if exists playlist.songs;

-- Create the songs table
-- star_rating is a column that will be used to store the user's rating of the song
-- Ideally rating would be a separate table with a FK to the songs table, and user_id as a FK to the users table
create table if not exists playlist.songs (
    id text primary key,
    title text not null,
    danceability float,
    energy float,
    key integer,
    loudness float,
    mode integer,
    acousticness float,
    instrumentalness float,
    liveness float,
    valence float,
    tempo float,
    duration_ms integer,
    time_signature integer,
    num_bars integer,
    num_sections integer,
    num_segments integer,
    class text,
    star_rating float not null default 0
);

-- index on the title column, searching on title for API
create index idx_title on songs (title);

-- Updates to table
ALTER TABLE playlist.songs RENAME COLUMN star_rating TO rating;
ALTER TABLE playlist.songs ADD rating_count int DEFAULT 0 not NULL;

