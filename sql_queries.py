import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
ARN = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (
                            artist varchar,
                            auth varchar,
                            firstName varchar,
                            gender varchar,
                            itemInSession integer,
                            lastName varchar,
                            length float,
                            level varchar,
                            location varchar,
                            method varchar,
                            page varchar,
                            registration float,
                            sessionId integer,
                            song varchar,
                            status varchar,
                            ts BIGINT,
                            userAgent varchar,
                            userId integer)
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (
                            num_songs integer,
                            artist_id varchar,
                            artist_latitude float,
                            artist_longitude float,
                            artist_location varchar,
                            artist_name varchar,
                            song_id varchar,
                            title varchar,
                            duration float,
                            year integer)
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay (
                        songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
                        start_time timestamp,
                        user_id integer,
                        level varchar,
                        song_id varchar,
                        artist_id varchar,
                        session_id integer,
                        location varchar,
                        user_agent varchar)
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                    user_id integer PRIMARY KEY,
                    first_name varchar,
                    last_name varchar,
                    gender varchar,
                    level varchar)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS song (
                    song_id varchar PRIMARY KEY,
                    title varchar,
                    artist_id varchar,
                    year integer,
                    duration float) 
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist (
                       artist_id varchar PRIMARY KEY,
                       name varchar,
                       location varchar,
                       latitude float,
                       longitude float)
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                    start_time timestamp PRIMARY KEY,
                    hour integer,
                    day integer,
                    week integer,
                    month integer,
                    year integer,
                    weekday integer)
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events from {} credentials 'aws_iam_role={}' format as json {} STATUPDATE ON region 'us-west-2'
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""copy staging_songs from {} credentials 'aws_iam_role={}' format as json 'auto' STATUPDATE ON region 'us-west-2'
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                        SELECT DISTINCT timestamp 'epoch' + se.ts/1000 * interval '1 second' AS start_time, se.userId AS user_id, se.level, ss.song_id, ss.artist_id, 
                        se.sessionId AS session_id, se.location, se.userAgent AS user_agent 
                        from staging_events se 
                        JOIN staging_songs ss 
                        ON (se.artist = ss.artist_name) 
                        where se.page = 'NextSong';
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                    SELECT DISTINCT userId AS user_id, firstName AS first_name, lastName AS last_name, gender, level from staging_events where page = 'NextSong';
""")

song_table_insert = ("""INSERT INTO song (song_id, title, artist_id, year, duration)
                    SELECT DISTINCT song_id, title, artist_id, year, duration from staging_songs where song_id is NOT NULL;
""")

artist_table_insert = ("""INSERT INTO artist (artist_id, name, location, latitude, longitude)
                      SELECT DISTINCT artist_id, artist_name AS name, artist_location AS location,
                      artist_latitude AS latitude, artist_longitude AS longitude
                      from staging_songs where artist_id is NOT NULL;
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                    SELECT start_time, EXTRACT(hour FROM start_time) AS hour,
                    EXTRACT(day FROM start_time) AS day,
                    EXTRACT(week FROM start_time) AS week,
                    EXTRACT(month FROM start_time) AS month,
                    EXTRACT(year FROM start_time) AS year,
                    EXTRACT(dayofweek FROM start_time) AS weekday from songplay;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]