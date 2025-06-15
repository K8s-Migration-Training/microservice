from flask import Flask, jsonify, request
import psycopg2
import os
import time
import requests

app = Flask(__name__)

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "eventsdb"),
    "user": os.getenv("POSTGRES_USER", "user"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "db"),
    "port": 5432,
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)
        cur.execute("SELECT COUNT(*) FROM events;")
        if cur.fetchone()[0] == 0:
            cur.execute("""
                INSERT INTO events (name) VALUES
                ('Konzert A'),
                ('Konferenz B'),
                ('Festival C');
            """)
        conn.commit()
        cur.close()
        conn.close()
        print("Datenbank initialisiert.")
    except Exception as e:
        print(f"Fehler bei DB-Init: {e}")

@app.route('/')
def list_events():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM events;")
        events = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(events)
    except Exception as e:
        print(f"Fehler beim Abrufen: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/book_event', methods=['POST'])
def book_event():
    
    response = requests.get('http://ticketservice:5000')
    ticket_data = response.text

    return jsonify({
        "ticket": ticket_data
    })

init_db()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
