from flask import Flask, jsonify, request
import psycopg2
import os
import time
import requests
import logging

app = Flask(__name__)

# Logging-Konfiguration
logging.basicConfig(level=logging.DEBUG if os.getenv("FLASK_ENV") == "development" else logging.INFO)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "eventsdb"),
    "user": os.getenv("POSTGRES_USER", "user"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "db"),
    "port": 5432,
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

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
        logger.info("Datenbank initialisiert.")
    except Exception as e:
        logger.exception("Fehler bei der Initialisierung der Datenbank.")

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
        logger.exception("Fehler beim Abrufen der Events.")
        return jsonify({"error": "Fehler beim Abrufen der Events", "details": str(e)}), 500

@app.route('/book_event', methods=['POST'])
def book_event():
    try:
        response = requests.get('http://ticketservice:5000')
        ticket_data = response.text
        return jsonify({"ticket": ticket_data})
    except Exception as e:
        logger.exception("Fehler beim Buchen des Events.")
        return jsonify({"error": "Fehler beim Buchen des Events", "details": str(e)}), 500

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
