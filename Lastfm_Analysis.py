import pylast
import pandas as pd
import matplotlib.pyplot as plt
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

lf = pylast.LastFMNetwork(
    api_key=os.getenv("LASTFM_API_KEY"),
    api_secret=os.getenv("LASTFM_API_SECRET")
)
#Dracula by Tame Impala URL
track_url = "https://www.last.fm/music/Tame+Impala/Dracula"

#extract the artist and track name from the URl Using Regular Expressions
track_id = re.search(r"music/(.*?)/(.*)" , track_url)

#fetch track details
def get_track_json(artist, track):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getInfo",
        "api_key": "8e862af14d93b5b3493447da6b50878d",
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

#display the metadata
print(f"Track Name: {track_data['Track Name']}")
print(f"Artist: {track_data['Artist']}")
print(f"Album: {track_data['Album']}")
print(f"Popularity: {track_data['Popularity']}")
print(f"Duration: {track_data['Duration']}")
print(f"Listeners: {track_data['Listeners']}")

#convert metadata into a pandas DataFrame
df=pd.DataFrame([track_data])
print("Track Metadata DataFrame:")
print(df)

#save metadata to a CSV file
df.to_csv("track_metadata.csv", index=False)


#visualize the bar chart
features = ['Popularity', 'Duration', 'Listeners']
values =[int(track_data['Popularity']), int(track_data['Duration']), int(track_data['Listeners'])]

plt.figure(figsize=(8, 6))
plt.bar(features, values, color=['blue', 'orange', 'green'], edgecolor='black')
plt.title(f"Track Metadata for '{track_data['Track Name']}' by {track_data['Artist']}")
plt.yscale('log')
plt.ylabel('Values')
plt.xlabel('Features')
plt.show()


