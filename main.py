from flask import Flask
from lineoa import lineoa_webhook
from db import db_operations

app = Flask(__name__)

@app.before_first_request
def initialize():
    db_operations.initialize_db()

@app.route("/webhook", methods=["POST"])
def webhook():
    return lineoa_webhook.handle_webhook()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
