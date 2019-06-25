from flask import Flask, render_template, jsonify, redirect
import scrape_mars2
from flask_pymongo import PyMongo

app = Flask(__name__)

# conn = 'mongodb://localhost:27017'
# client = PyMongo.MongoClient(conn)

# db = client.mars
# collection = db.mars

# mongo = PyMongo(app)

# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return  render_template('index.html', mars=mars)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars2.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)