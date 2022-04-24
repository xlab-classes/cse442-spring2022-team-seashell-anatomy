from encodings import utf_8
import numpy as np
from functools import reduce
from db import SONG_DATA, ENGINE,shared_playlists
from spotify_api import get_songs
#from __init__ import SONG_DATA, ENGINE
import random
from views import rec
import json
#Merges two dictionaries into one.
def Merge(dict1, dict2):
    return(dict2.update(dict1))

def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

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

def get_song_by_uri(uri):
   print(uri)
   s = SONG_DATA.select().where(SONG_DATA.c.id == uri) #SELECT * FROM SONG_DATA WHERE 'id' = isong_d
   conn = ENGINE.connect()
   result = conn.execute(s)
   song_list = []

   #print(song_list)

   for rows in result: #Appends all columns in the table that contain the specific id into song_list
      song_list.append(dict(rows))

   if(len(song_list) == 0): #If list is empty, the database does not contain this song.
      print('Insert this song in the database!')
      return -1

   print("This song is already in the database!")
   return song_list[0]

def insert_song(id):
      song_dic =  get_songs.get_one_song(id) #Populates a list of dictionaries containing the song data.
      song_dic = dict(song_dic)

      Merge(song_dic['song_features'], song_dic) #Takes song features and separates them to match exact formatting.
      song_dic.pop('song_features')       #Removes the song_features dict from the song data.
      print(song_dic)
      song_dic['artist_name'] = listToString(song_dic['artist_name']) #Converts the artist names into a string.

      ins = SONG_DATA.insert().values(**song_dic)
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
    print(rec.prev_songs())
    old = json.loads(rec.prev_songs())
    #print("result type", type(result))
    #print(type(result[0]))
    for s in result:
       if s['id'] in old:
          result.remove(s)
    if len(result) > 10:
        return random.choices(result, k=10)
    else:
        return result


def get_songs_by_attr(attr, min, max):
    s = SONG_DATA.select().where(SONG_DATA.c[attr] <= max, SONG_DATA.c[attr] >= min)
    conn = ENGINE.connect()
    result = [dict(x) for x in conn.execute(s)]
    return result
