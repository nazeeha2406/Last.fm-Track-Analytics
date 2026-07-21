import pylast
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

lf = pylast.LastFMNetwork(
    api_key=os.getenv("LASTFM_API_KEY"),
    api_secret=os.getenv("LASTFM_API_SECRET")
)


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv("MYSQL_PASSWORD"),
    'database': 'LastFm'
}

#connect to the database
connection= mysql.connector.connect(**db_config)
cursor=connection.cursor()

#full track URL
track_url = "https://www.last.fm/music/Tame+Impala/Dracula"

#extract trackid from the URL using regular expressions
track_id= re.search(r"music/(.*?)/(.*)" , track_url)

def get_track_json(artist, track):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getInfo",
        "api_key": os.getenv("LASTFM_API_KEY"),
        "artist": artist,
        "track": track,
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()

track= get_track_json("Tame Impala", "Dracula")
#print(track)

#extract metadata from the track data
track_data={'Track Name': track['track']['name'],
                'Artist' : track['track']['artist']['name'],
                'Album' : track['track']['album']['title'],
                'Popularity' : track['track']['playcount'],
                'Duration' : int(track['track']['duration']),  # Convert milliseconds to seconds
                'Listeners' : track['track']['listeners']}

#insert data in mysql
insert_query = """
insert into lastfm_tracks (track_name, artist, album, popularity, duration, listeners)
values (%s, %s, %s, %s, %s, %s)
"""

cursor.execute(insert_query,
               (track_data['Track Name'], track_data['Artist'], track_data['Album'],
                track_data['Popularity'], track_data['Duration'], track_data['Listeners']))

connection.commit()

print(f"{track_data['Track Name']} by {track_data['Artist']} - Data inserted into the database successfully.")

cursor.close()
connection.close()
