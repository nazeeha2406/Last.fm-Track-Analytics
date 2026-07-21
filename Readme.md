# 🎵 Last.fm Track Analytics

A Python project that fetches track metadata from the **Last.fm API**, analyzes it, stores it in **MySQL**, and visualizes key metrics (popularity, duration, listeners) using Matplotlib.

## 📌 Features

- Fetch full track metadata (name, artist, album, popularity, duration, listeners) from Last.fm's `track.getInfo` API
- Parse artist/track names directly from Last.fm track URLs using regex
- Store track data in a MySQL database for persistent storage
- Batch-process a list of track URLs from a text file
- Visualize track metadata as a bar chart (log scale to handle large value differences)
- Export track metadata to CSV

## 📂 Project Structure

| File | Description |
|---|---|
| `lastfm_single_track.py` | Fetches metadata for a single track, saves to CSV, and plots a bar chart |
| `lastfm_to_mysql.py` | Fetches metadata for a single track and inserts it into a MySQL database |
| `lastfm_batch_to_mysql.py` | Reads multiple track URLs from `track_urls.txt`, fetches metadata for each, and inserts them all into MySQL |
| `track_urls.txt` | Text file containing Last.fm track URLs (one per line) |

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install pylast pandas matplotlib mysql-connector-python requests
```

### 2. Get a Last.fm API key

Register for a free API key at [last.fm/api/account/create](https://www.last.fm/api/account/create).

### 3. Configure your credentials

Replace the placeholders in each script with your own:

```python
lf = pylast.LastFMNetwork(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")
```

```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',
    'database': 'LastFm'
}
```

> ⚠️ **Note:** Don't commit real API keys or DB passwords to GitHub. Use environment variables or a `.env` file (see [Security Note](#-security-note) below).

### 4. Create the MySQL table

```sql
CREATE DATABASE IF NOT EXISTS LastFm;
USE LastFm;

CREATE TABLE IF NOT EXISTS lastfm_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    track_name VARCHAR(255),
    artist VARCHAR(255),
    album VARCHAR(255),
    popularity BIGINT,
    duration INT,
    listeners BIGINT
);
```

### 5. Prepare your track URL list (for batch processing)

Create `track_urls.txt` with one Last.fm track URL per line:

```
https://www.last.fm/music/Ed+Sheeran/_/Perfect
https://www.last.fm/music/Tame+Impala/_/Dracula
https://www.last.fm/music/Shawn+Mendes/_/Senorita
```

## 🚀 Usage

**Single track → CSV + chart:**
```bash
python lastfm_single_track.py
```

**Single track → MySQL:**
```bash
python lastfm_to_mysql.py
```

**Batch tracks (from `track_urls.txt`) → MySQL:**
```bash
python lastfm_batch_to_mysql.py
```

## 📊 Sample Output

```
Track Name: Dracula
Artist: Tame Impala
Album: InnerSpeaker
Popularity: 245891
Duration: 205000
Listeners: 89234
```

A bar chart (log-scaled) comparing Popularity, Duration, and Listeners is displayed and can be saved from the plot window.

## 🛠️ Tech Stack

- [pylast](https://github.com/pylast/pylast) — Python wrapper for the Last.fm API
- [requests](https://docs.python-requests.org/) — Direct REST calls to Last.fm's `track.getInfo`
- [pandas](https://pandas.pydata.org/) — Data structuring and CSV export
- [matplotlib](https://matplotlib.org/) — Data visualization
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) — MySQL database integration

## 🔐 Security Note

This repo's scripts currently show API keys and DB passwords inline for simplicity. Before pushing to GitHub, it's recommended to move secrets to environment variables:

```python
import os
api_key = os.getenv("LASTFM_API_KEY")
db_password = os.getenv("MYSQL_PASSWORD")
```

Add a `.env` file (and add `.env` to `.gitignore`) to keep credentials out of version control.

## 📝 Known Limitations

- Last.fm identifies tracks by **artist + track name** (not a unique ID like Spotify), so mismatched spellings can cause lookup failures
- Some tracks may be missing metadata fields (e.g. album, mbid) if not fully tagged on Last.fm
- No retry/rate-limit handling for large batch runs — consider adding delays for big URL lists

## 📄 License

MIT License — feel free to use and modify.