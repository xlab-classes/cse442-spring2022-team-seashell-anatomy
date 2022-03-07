from multiprocessing import connection
import mysql.connector
import pickle
from sqlalchemy import Float, PickleType, create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, inspect
import spotify 
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://jrnaranj:50309202@oceanus.cse.buffalo.edu/cse442_2022_spring_team_b_db', echo = True)
engine.connect()

#print(engine) #Verifies that the connection was successful.

#print(engine.table_names())  #Gets the table names

#print(spotify.audio_features[0])

meta = MetaData()

song_data = Table(
   'song_data', meta, 
   Column('id_number', Integer, primary_key = True), 
   Column('song_name', String(255)), 
   Column('artist_name', String(255)),
   Column('genre_list', PickleType),
   Column('cover_art', String(255)),
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
   Column('id', String(255)),
   Column('uri', String(255)),
   Column('track_href', String(255)),
   Column('analysis_url', String(255)),
   Column('duration_ms', Float),
   Column('time_signature', Integer)

)

meta.create_all(engine)


#print(len(spotify.track_name))

obj_list = []

Session = sessionmaker(bind=engine)

session = Session()

#data_obj = Table(**spotify.audio_features[0])
audio_features = spotify.audio_features[0]

ins = song_data.insert()
ins = song_data.insert().values(**audio_features[0])
conn = engine.connect()
result = conn.execute(ins)







