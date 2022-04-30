from get_songs import get_songs
from sqlalchemy import Float, PickleType, create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from db import SONG_DATA, ENGINE, shared_playlists, song_dict
#from __init__ import SONG_DATA, ENGINE, shared_playlists, song_dict
import pickle

# As of now, populate_database will not account for duplicates. If run multiple times there will be columns with the same song in it.
# Working on a fix now, if you wish to use populate_database, first drop the table ( DROP TABLE song_name) and then rerun the function.


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

def populate_database(num_songs):

    for f in song_dict:
       Merge(f['song_features'], f) #Takes song features and separates them to match exact formatting.
       f.pop('song_features')       #Removes the song_features dict from the song data.
       f['artist_name'] = listToString(f['artist_name']) #Converts the artist names into a string.
    
    print(song_dict)
    for i in range(num_songs): #Populates the database with the number of songs
       ins = SONG_DATA.insert().values(**song_dict[i])
       conn = ENGINE.connect()
       conn.execute(ins)

def populate_share(share_list, attr):
       pickle.dumps(share_list)

       ins = shared_playlists.insert().values(
           playlist = share_list,
           acousticness = attr['acousticness'],
           danceability = attr['danceability'],
           energy = attr['energy'],
           valance = attr['valance']
        )
       conn = ENGINE.connect()
       conn.execute(ins)

#populate_database(1000)
