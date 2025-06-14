from flask import Flask, jsonify
import psycopg2
import os
import time

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

@app.route('/')
def list_events():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM events;")
    events = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
