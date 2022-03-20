import unittest
from db.songs import get_songs_by_attrs


class TestAttributes(unittest.TestCase):
    # test that the songs returned by 
    # get_songs_by_attrs() are unique
    def test_get_song_by_attrs_unique(self):
        attrs = [('speechiness', 0.0, 0.5), ('energy', 0.0, 1)]
        playlist = get_songs_by_attrs(attrs)

        songs = set()
        for song in playlist:
            self.assertTrue(song['id_number'] not in songs)
            songs.add(song['id_number'])
        
    # test that the attributes of the returned songs
    # are within the bounds min <= attr <= max
    def test_attrs_in_specified_range(self):
        attrs = [('speechiness', 0.0, 0.5), ('energy', 0.0, 1)]
        playlist = get_songs_by_attrs(attrs)

        for song in playlist:
            for attr, min, max in attrs:
                self.assertTrue(min <= song[attr] <= max)


if __name__ == '__main__':
    unittest.main()
