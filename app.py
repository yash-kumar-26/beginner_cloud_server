from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Cloud File Storage Backend Running"

if __name__ ==  "__main__":
    app.run(debug=True)