from spotify_api.spotify import get_data
from db import SONG_DATA, ENGINE


# As of now, populate_database will not account for duplicates. If run multiple times there will be columns with the same song in it.
# Working on a fix now, if you wish to use populate_database, first drop the table ( DROP TABLE song_name) and then rerun the function.

def populate_database(year, num_songs):
   song_dict = get_data(year, num_songs) #Populates a list of dictionaries containing the song data.

   for i in range(num_songs): #Populates the database with the number of songs
      ins = SONG_DATA.insert().values(**song_dict[i])
      conn = ENGINE.connect()
      conn.execute(ins)
