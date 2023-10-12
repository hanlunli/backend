
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import random, time

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

class Message():
    def getid(self):
        return self.id
    def getusername(self):
        return self.username
    def getmessage(self):
        return self.message
    def gettime(self):
        return self.time
    
    def __init__(self, id, username, message, time):
        self.id = id
        self.username = username
        self.message = message
        self.time = time

# ... your existing Flask
# add an api endpoint to flask app
@app.route('/messageDB', methods=["POST", "GET"])
def messageDB(message):
    messagedata = {"id": message.getid(),
                   "username": message.getusername(),
                   "message": message.getmessage(),
                   "time": message.gettime()}
    return messagedata

@app.route('/wpmtest', methods=["GET"])
def get_data():
    global test_data
    global rand
    global start

    dictionary = open("words.txt", "r")
    temp = dictionary.readlines()
    dictionary.close()
    listwords = []

    for i in temp:
        listwords.append(i.strip())

    start = time.perf_counter()

    test_data = []
    usedlist = []
    while True: #iteration
        temp2 = random.randint(0, len(listwords))
        print(temp2)
        if temp2 not in usedlist: #usedlist is a list of the indexes of random words that we've already used
            usedlist.append(temp2)
            test_data.append(listwords[temp2]) #test_data is the final list of words that the user's input will be compared to
        if len(test_data) == 50:
            break
        
    rand = random.randint(0,len(test_data)-1)
    temp3 = ''

    for i in test_data: #iteration
        temp3 += i + ' '
    return (temp3+render_template('wtf.md'))

@app.route('/inputdata', methods=["POST"])
def inputdata():
    html_content = """<html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
    <style>
    .headerbutton {
    border: 1px solid #5f73b8;
    background: #424549;
    color: white;
    width: 270px;
    padding: 15px 20px;
    font-weight: bold;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 15px;
    transition-duration: 0.1s;
    cursor: pointer;
    font-family: serif;
    }
    .headerbutton:hover{
    background:  #7e92d6;
    /* color: rgb(78, 3, 66); */
    }
    body {
    text-align: center;
    padding: 25px;
    background-color: #121212;
    color: #7e92d6;
    font-size: 24px;
    font-weight: bold;
    transition-duration: 0.2s;
   }
    </style>
    <button id="border"type="button" class="headerbutton" onclick="window.location.href='/wpmtest';">Do the test again</button> <br \>  
    </body>
    </html>"""
    print(test_data[rand])
    words = request.form['a']
    end = time.perf_counter();
    totalTime = end - start;
    total = 0;
    word = words
    words = words.split();
    data = test_data;
    untotal = 0

    all = 0;
    if(len(data) > len(words)):
        for i in range(len(words)):
            if data[i] == words[i]:
                total+=1;
            all += 1;
    else:
        for i in range(len(data)):
            if data[i] == words[i]:
                total+=1;
            all += 1;

    # total = all - untotal #all is the number of total words, untotal is the number of incorrect words, total - incorrect = correct.

    html_content += "<br> <br><br>"
    try:
        html_content+= "Accuracy: " + str((total/all*100)//1)+ "%" + '\n' #calculates wpm in % by dividing total words correct by all words inputted, then multiplying by 100
    except:
        pass;
    
    html_content += "WPM: " + str((total/(totalTime)*60)//1) + '\n' #calculates wpm by dividing words correct by time it took to type the words
    return html_content
@app.route('/')
def say_hello():
    return render_template('main.md')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True)
