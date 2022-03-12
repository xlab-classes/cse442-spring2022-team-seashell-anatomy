from multiprocessing import connection
import mysql.connector
import pickle
from sqlalchemy import Float, PickleType, create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, inspect
import spotify 
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://jrnaranj:50309202@oceanus.cse.buffalo.edu/cse442_2022_spring_team_b_db', echo = True)
engine.connect()

meta = MetaData()

song_data = Table(
   'song_data', meta, 
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

meta.create_all(engine)




obj_list = []

Session = sessionmaker(bind=engine)

session = Session()



def populate_database(year, num_songs):
   song_dict = spotify.get_data(2019, num_songs) #Populates a list of dictionaries containing the song data.

   for i in range(num_songs): #Populates the database with the number of songs
      ins = song_data.insert()
      ins = song_data.insert().values(**song_dict[i])
      conn = engine.connect()
      result = conn.execute(ins)

# As of now, populate_database will not account for duplicates. If run multiple times there will be columns with the same song in it.
# Working on a fix now, if you wish to use populate_database, first drop the table ( DROP TABLE song_name) and then rerun the function.

#populate_database(2019,50)



def get_song_by_name(song_name):
   s = song_data.select().where(song_data.c.song_name== song_name ) #SELECT * FROM song_data WHERE 'song_name' = song_name
   conn = engine.connect()
   result = conn.execute(s)
   song_list = []

   for rows in result: #Appends all columns in the table that contain the song name into song_list
      song_list.append(dict(rows))

   if(len(song_list) == 0): #If list is empty, the database does not contain this song.
      print('This song is not in the database!')

   return song_list

def get_song_by_id(id):
   s = song_data.select().where(song_data.c.song_id== id ) #SELECT * FROM song_data WHERE 'id' = isong_d
   conn = engine.connect()
   result = conn.execute(s)
   song_list = []

   for rows in result: #Appends all columns in the table that contain the specific id into song_list
      song_list.append(dict(rows))

   if(len(song_list) == 0): #If list is empty, the database does not contain this song.
      print('This song is not in the database!')

   return song_list

def get_song_by_artist(artist_name):
   s = song_data.select().where(song_data.c.artist_name == None ) #SELECT * FROM song_data WHERE 'id' = isong_d
   conn = engine.connect()
   result = conn.execute(s)
   song_list = []

   for rows in result: #Appends all columns in the table that contain the artist into song_list
      song_list.append(dict(rows))

   if(len(song_list) == 0): #If list is empty, the database does not contain this song.
      print('This song is not in the database!')

   return song_list








