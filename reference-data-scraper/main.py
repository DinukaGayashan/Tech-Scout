from flask import Flask,request,jsonify
from scrape import testscrape,scrape_all
from retrieve import retrieve_all


app=Flask(__name__)

@app.route("/")
def home():
    
    return (testscrape())

@app.route("/scrape-all", methods=["POST"])
def scrapeAll():
    scrape_all()  
    return jsonify("scrape done",200)

@app.route("/get-all")
def getData():
    categories = ["CPU", "VideoCard", "Memory", "Motherboard", "Monitor", "Keyboard"]
    return retrieve_all(categories)


if __name__=="__main__":
    app.run(debug=True)