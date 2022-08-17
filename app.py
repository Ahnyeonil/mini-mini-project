# 패키지 설치 -> flask, pymongo, dnspython

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://ahn:sparta@cluster0.s9tldtb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbprestudy

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/new_member')
def newMember_page():
    return render_template('new_member.html')

#@app.route("/mars", methods=["POST"])
#def web_mars_post():
#sample_receive = request.form['sample_give']
#print(sample_receive)
#return jsonify({'msg': 'POST 연결 완료!'})

#@app.route("/mars", methods=["GET"])
#def web_mars_get():
#return jsonify({'msg': 'GET 연결 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)