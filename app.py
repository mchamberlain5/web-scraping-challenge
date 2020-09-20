from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

app.config['MONGO_URI']='MONGODB://localhost:27017/mars_app'
mongo = PyMongo(app)

@app.route("/")
def index():
	results=mongo.db.mars.find_one()
	return render_template("index.html",mars_data = results)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)