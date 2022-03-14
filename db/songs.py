from db import SONG_DATA, ENGINE


def get_song_by_name(song_name):
   s = SONG_DATA.select().where(SONG_DATA.c.song_name == song_name) #SELECT * FROM SONG_DATA WHERE 'song_name' = song_name
   conn = ENGINE.connect()
   result = conn.execute(s)
   song_list = []

   for rows in result: #Appends all columns in the table that contain the song name into song_list
      song_list.append(dict(rows))

   if(len(song_list) == 0): #If list is empty, the database does not contain this song.
      print('This song is not in the database!')

   return song_list


def get_song_by_id(id):
   s = SONG_DATA.select().where(SONG_DATA.c.song_id == id) #SELECT * FROM SONG_DATA WHERE 'id' = isong_d
   conn = ENGINE.connect()
   result = conn.execute(s)
   song_list = []

   for rows in result: #Appends all columns in the table that contain the specific id into song_list
      song_list.append(dict(rows))

   if(len(song_list) == 0): #If list is empty, the database does not contain this song.
      print('This song is not in the database!')

   return song_list


def get_song_by_artist(artist_name):
   s = SONG_DATA.select().where(SONG_DATA.c.artist_name == artist_name) #SELECT * FROM SONG_DATA WHERE 'id' = isong_d
   conn = ENGINE.connect()
   result = conn.execute(s)
   song_list = []

   for rows in result: #Appends all columns in the table that contain the artist into song_list
      song_list.append(dict(rows))

   if(len(song_list) == 0): #If list is empty, the database does not contain this song.
      print('This song is not in the database!')

   return song_list


def get_songs_by_attr(attr, min, max):
    s = SONG_DATA.select().where((SONG_DATA.c[attr] <= max) & (SONG_DATA.c[attr] >= min))
    conn = ENGINE.connect()
    result = conn.execute(s)
    return result

