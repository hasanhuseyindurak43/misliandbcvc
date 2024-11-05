from flask import Flask, render_template, request, redirect, url_for, session
import googleapiclient.discovery
import sqlite3
import datetime

# API anahtarınızı burada belirtin
api_key = "AIzaSyAdA2KJSYUaDn_MtWwFcdQsddhDSwcznTY"

# YouTube API istemcisini başlatma
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Flask session için gizli anahtar


# SQLite3 veritabanına bağlanma
def get_db_connection():
    conn = sqlite3.connect('youtube_films.db')
    conn.row_factory = sqlite3.Row
    return conn


# Tabloyu oluşturma (eğer yoksa)
def create_tables():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS films
                    (title TEXT, video_id TEXT, duration TEXT, embed_code TEXT, total_seconds INTEGER)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, trust_level INTEGER, tl REAL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS user_actions
                    (user_id INTEGER, video_id TEXT, action TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, timestamp_seconds INTEGER)''')
    conn.commit()
    conn.close()


create_tables()


def get_film_category_id():
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode="US"
    )
    response = request.execute()

    for item in response['items']:
        if item['snippet']['title'].lower() == 'film & animation':
            return item['id']
    return None


def search_youtube_videos(query, film_category_id, min_duration="1H", max_duration="2H", max_results=50):
    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=query,
        type="video",
        videoDuration="long"
    )
    response = request.execute()

    videos = []

    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_details = youtube.videos().list(
            part="contentDetails,snippet",
            id=video_id
        ).execute()

        for video_detail in video_details['items']:
            duration = video_detail['contentDetails']['duration']
            category_id = video_detail['snippet']['categoryId']

            if category_id != film_category_id:
                continue

            hours = minutes = seconds = 0

            if 'H' in duration:
                hours = int(duration.split('H')[0].replace('PT', ''))
                duration = duration.split('H')[1]

            if 'M' in duration:
                minutes = int(duration.split('M')[0])
                duration = duration.split('M')[1]

            if 'S' in duration:
                seconds = int(duration.split('S')[0])

            total_seconds = hours * 3600 + minutes * 60 + seconds

            if total_seconds >= 3600 and total_seconds <= 7200:
                embed_code = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
                videos.append({
                    "title": video_title,
                    "video_id": video_id,
                    "duration": f"{hours}h {minutes}m {seconds}s",
                    "embed_code": embed_code,
                    "total_seconds": total_seconds
                })

    return videos


def save_to_sqlite(videos):
    conn = get_db_connection()
    cursor = conn.cursor()

    for video in videos:
        cursor.execute('''
            INSERT INTO films (title, video_id, duration, embed_code, total_seconds) 
            VALUES (?, ?, ?, ?, ?)
        ''', (video['title'], video['video_id'], video['duration'], video['embed_code'], video['total_seconds']))

    conn.commit()
    conn.close()


def update_user_tl(user_id, amount):
    conn = get_db_connection()
    conn.execute('UPDATE users SET tl = tl + ? WHERE id = ?', (amount, user_id))
    conn.commit()
    conn.close()


def update_user_trust(user_id, change):
    conn = get_db_connection()
    conn.execute('UPDATE users SET trust_level = trust_level + ? WHERE id = ?', (change, user_id))
    conn.commit()
    conn.close()


def get_video_progress(user_id, video_id):
    conn = get_db_connection()
    progress = conn.execute(
        'SELECT timestamp_seconds FROM user_actions WHERE user_id = ? AND video_id = ? AND action = "progress" ORDER BY timestamp DESC LIMIT 1',
        (user_id, video_id)).fetchone()
    conn.close()
    return progress['timestamp_seconds'] if progress else 0


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        film_category_id = get_film_category_id()
        if film_category_id:
            videos = search_youtube_videos(query, film_category_id)
            save_to_sqlite(videos)
            return redirect(url_for('index'))

    conn = get_db_connection()
    films = conn.execute('SELECT * FROM films').fetchall()
    conn.close()
    return render_template('deneme1.html', films=films)


@app.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return render_template('profile.html', user=user)
    return redirect(url_for('index'))


@app.route('/video/<video_id>', methods=['GET'])
def video(video_id):
    conn = get_db_connection()
    video = conn.execute('SELECT * FROM films WHERE video_id = ?', (video_id,)).fetchone()
    conn.close()
    return render_template('video.html', video=video)


@app.route('/user_action', methods=['POST'])
def user_action():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    action = request.form['action']
    video_id = request.form['video_id']
    timestamp_seconds = int(request.form['timestamp_seconds'])

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO user_actions (user_id, video_id, action, timestamp, timestamp_seconds) VALUES (?, ?, ?, ?, ?)',
        (user_id, video_id, action, datetime.datetime.now(), timestamp_seconds))
    conn.commit()

    if action == 'end':
        update_user_tl(user_id, 0.00010)
    elif action == 'skip':
        update_user_trust(user_id, -1)
    elif action == 'finish':
        update_user_trust(user_id, 1)

    conn.close()
    return redirect(url_for('video', video_id=video_id))


if __name__ == '__main__':
    app.run(debug=True)
