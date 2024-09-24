from flask import Flask, render_template, request, jsonify

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
def getdata():
    data = request.json
    subreddit = data.get('subreddit')
    
    ## Api data check here #########
    
    post_count = "1000"    
    comment_count = "1456"
    
    mostusedword_1 = "Popa"
    mostusedword_2 = "Booty"
    mostusedword_3 = "Juicy"
    mostusedword_4 = "Spank"
    mostusedword_5 = "Bubu"   
    
    attitude_result = "Very Positive"
    attitude_rating = "95"
    
    return jsonify({
        'post_count': post_count,
        'comment_count': comment_count,        
        'mostusedword_1': mostusedword_1,        
        'mostusedword_2': mostusedword_2,        
        'mostusedword_3': mostusedword_3,        
        'mostusedword_4': mostusedword_4,
        'mostusedword_5': mostusedword_5,
        'attitude_result': attitude_result,
        'attitude_rating': attitude_rating
    })

if __name__ == '__main__':
    # You can specify the port here
    app.run(debug=True, host='0.0.0.0', port=5001)