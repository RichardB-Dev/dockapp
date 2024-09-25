from flask import Flask, render_template, request, jsonify,Response


import praw
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import io
import os
import api

app = Flask(__name__)
print("Flask app is starting")

@app.route('/')
def home():
    print("Load Page 1")
    return render_template('index.html')


@app.route('/test')
def test():
    print("Load Test Page")
    return "Hello, Flask Is Working!"
    
@app.route('/getdata', methods=['POST'])
def getdata2():
    data = request.json
    subreddit = data.get('subreddit')
    word = data.get('word')
    
    result = api.datacheck(subreddit, word)    
    return result  

if __name__ == '__main__':
    # You can specify the port here
    app.run(debug=True, host='0.0.0.0', port=5001)
    #app.run(ssl_context=('cert.pem', 'key.pem'), debug=True, host='0.0.0.0')