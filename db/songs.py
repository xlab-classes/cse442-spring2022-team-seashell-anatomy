import numpy as np
from functools import reduce
from db import SONG_DATA, ENGINE,shared_playlists
#from __init__ import SONG_DATA, ENGINE

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
      return -1

   return song_list[0]

def insert_song(id):
      ins = SONG_DATA.insert().values(uri = id)
      conn = ENGINE.connect()
      conn.execute(ins)


def get_shared():
   s= shared_playlists.select()
   conn = ENGINE.connect()
   result = conn.execute(s)
   song_list = []

   for rows in result: 
      song_list.append(dict(rows))
   
   return song_list

def get_playlist_with_id(share_list):

   playlist = []

   for i in share_list:
      playlist.append(get_song_by_id(i['song_id']))
   
   return playlist


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


# input list of lists, output intersection of lists
def set_and(lists):
    ids = reduce(np.intersect1d, tuple([x['id_number'] for x in _] for _ in lists))
    
    retval = []
    added_ids = set()
    for _list in lists:
        for song in _list:
            _id = song['id_number']
            if _id in ids and _id not in added_ids:
                retval.append(song)
                added_ids.add(_id)

    return retval


# {'name': attrA, 'min': 3, 'max': 7}
def get_songs_by_attrs(attrs):
    song_attrs = []
    for attr, min, max in attrs:
        song_attrs.append(get_songs_by_attr(attr, min, max))

    result = set_and(song_attrs)
    return result


def get_songs_by_attr(attr, min, max):
    s = SONG_DATA.select().where(SONG_DATA.c[attr] <= max, SONG_DATA.c[attr] >= min).limit(10)
    conn = ENGINE.connect()
    result = [dict(x) for x in conn.execute(s)]
    return result


def toggle_upvote(song_id):
   pass 
