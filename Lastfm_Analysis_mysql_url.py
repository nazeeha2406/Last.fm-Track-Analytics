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
with open("track_urls.txt",'r')as f:
    track_urls=f.readlines()

for track_url in track_urls:
    try:
        track_url = track_url.strip()  # Remove any leading/trailing whitespace or newline characters
        #extract trackid from the URL using regular expressions
        track_id = re.search(r"music/(.*?)/_/(.*)", track_url)

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

        track= get_track_json(track_id.group(1).replace('+', ' '), track_id.group(2).replace('+', ' '))
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

    except Exception as e:
        print(f"Error processing track URL {track_url}: {e}")

cursor.close()
connection.close()

print("All track data has been processed and inserted into the database.")
