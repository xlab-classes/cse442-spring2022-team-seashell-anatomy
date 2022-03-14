from sqlalchemy import Float, PickleType, create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine('mysql+pymysql://jrnaranj:50309202@oceanus.cse.buffalo.edu/cse442_2022_spring_team_b_db', echo = True)
ENGINE.connect()
META = MetaData()
SONG_DATA = Table(
   'song_data', META, 
   Column('id_number', Integer, primary_key = True), 
   Column('song_name', String(255)), 
   Column('artist_name', String(255)),
   Column('genre_list', PickleType),
   Column('cover_url', String(255)),
   Column('danceability', Float),
   Column('energy', Float),
   Column('key', Float),
   Column('loudness', Float),
   Column('mode', Float),
   Column('speechiness', Float),
   Column('acousticness', Float),
   Column('instrumentalness', Float),
   Column('liveness', Float),
   Column('valence', Float),
   Column('tempo', Float),
   Column('type', String(255)),
   Column('song_id', String(255)),
   Column('id', String(255)),
   Column('uri', String(255)),
   Column('track_href', String(255)),
   Column('analysis_url', String(255)),
   Column('duration_ms', Float),
   Column('time_signature', Integer),
   Column('rating', Float)
)

META.create_all(ENGINE)
SESSION = sessionmaker(bind=ENGINE)()
