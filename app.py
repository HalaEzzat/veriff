from flask import Flask
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    logger.info("Home page accessed")
    return "Hello, Veriff Observability!"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/ready")
def ready():
    return "Ready", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
