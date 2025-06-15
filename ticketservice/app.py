from flask import Flask, jsonify
import uuid

app = Flask(__name__)

@app.route('/')
def createticket():
    ticket_id = str(uuid.uuid4())
    return jsonify({"ticket_id": ticket_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
