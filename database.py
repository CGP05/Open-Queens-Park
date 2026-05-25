import sqlite3
from datetime import datetime

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parties (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            abbreviation TEXT,
            color TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS speakers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            party_id INTEGER,
            constituency TEXT,
            FOREIGN KEY (party_id) REFERENCES parties(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            session_date DATE UNIQUE NOT NULL,
            parliament INTEGER,
            session INTEGER,
            url TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS speeches (
            id INTEGER PRIMARY KEY,
            speaker_id INTEGER,
            session_id INTEGER,
            text TEXT NOT NULL,
            timestamp TEXT,
            FOREIGN KEY (speaker_id) REFERENCES speakers(id),
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    ''')

    connection.commit()

def insert_party(name, abbreviation=None, color=None):
    try:
        cursor.execute('''
            INSERT INTO parties (name, abbreviation, color)
            VALUES (?, ?, ?)
        ''', (name, abbreviation, color))
        connection.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        cursor.execute('SELECT id FROM parties WHERE name = ?', (name,))
        return cursor.fetchone()[0]

def insert_speaker(name, party_id, constituency=None):
    cursor.execute('''
        INSERT OR IGNORE INTO speakers (name, party_id, constituency)
        VALUES (?, ?, ?)
    ''', (name, party_id, constituency))
    connection.commit()
    cursor.execute('SELECT id FROM speakers WHERE name = ?', (name,))
    return cursor.fetchone()[0]

def insert_session(session_date, parliament=None, session=None, url=None):
    try:
        cursor.execute('''
            INSERT INTO sessions (session_date, parliament, session, url)
            VALUES (?, ?, ?, ?)
        ''', (session_date, parliament, session, url))
        connection.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        cursor.execute('SELECT id FROM sessions WHERE session_date = ?', (session_date,))
        return cursor.fetchone()[0]

def insert_speech(speaker_id, session_id, text, timestamp=None):
    cursor.execute('''
        INSERT INTO speeches (speaker_id, session_id, text, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (speaker_id, session_id, text, timestamp))
    connection.commit()
    return cursor.lastrowid

def get_speeches_by_date(session_date):
    cursor.execute('''
        SELECT s.name, sp.text, sp.timestamp
        FROM speeches sp
        JOIN speakers s ON sp.speaker_id = s.id
        JOIN sessions ss ON sp.session_id = ss.id
        WHERE ss.session_date = ?
        ORDER BY sp.timestamp
    ''', (session_date,))
    return cursor.fetchall()

def close():
    connection.close()

create_tables()
