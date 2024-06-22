from flask import Flask, request
from blueprints.accident import accident_api
from blueprints.hidden_danger import hidden_danger_api

app = Flask(__name__)

app.register_blueprint(accident_api)
app.register_blueprint(hidden_danger_api)

if __name__ == "__main__":
    app.run(port=9002)
