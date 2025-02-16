from flask import Flask, request
import logging
import random
import time

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    app.logger.info("Home page visited")
    return "Hello, Kubernetes!"

@app.route("/metrics")
def metrics():
    return "request_count 1\nresponse_time " + str(random.uniform(0.1, 1.0))

@app.route("/error")
def error():
    app.logger.error("Error encountered!")
    return "Error occurred!", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
