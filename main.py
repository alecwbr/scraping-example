import datetime
import html
import sqlite3
import sys

from classes.KingFmApi import KingFmApi

kingfm_api = KingFmApi()

con = sqlite3.connect("database.sqlite3")
cur = con.cursor()

# get the last entry in table, only date_time_played column
latest_date_time = cur.execute("SELECT date_time_played FROM song_data WHERE date_time_played=(SELECT max(date_time_played) FROM song_data);").fetchone()
latest_date_time = latest_date_time[0] if latest_date_time is not None else None

# we reverse it because we want the latest song to be last in the table.
# fields we can use inside the 'track' array are:
# song, artist, art(object with small, medium fields), album, purchase, timestamp
if kingfm_api.fetched_songs_num == 0:
    sys.exit()

for song in reversed(kingfm_api.tracks):
    formatted_song = html.unescape(song['song'])
    formatted_artist = html.unescape(song['artist'])
    formatted_album = html.unescape(song['album'])
    formatted_timestamp = int(song['timestamp'])

    if latest_date_time:
        if formatted_timestamp > latest_date_time:
            cur.execute("INSERT INTO song_data(title, artist, album, date_time_played) VALUES (?, ?, ?, ?)", (formatted_song, formatted_artist, formatted_album, formatted_timestamp))
            print(f"{formatted_song} - {formatted_artist}")
    
    else:
        cur.execute("INSERT INTO song_data(title, artist, album, date_time_played) VALUES (?, ?, ?, ?)", (formatted_song, formatted_artist, formatted_album, formatted_timestamp))
        print(f"{formatted_song} - {formatted_artist}")

con.commit()
con.close()
