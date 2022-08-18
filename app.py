from flask import Flask, render_template, jsonify, request, session
from pymongo import MongoClient
from datetime import timedelta
from markupsafe import escape

client = MongoClient('mongodb+srv://test:sparta@cluster0.38yzx.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)
app.secret_key = 'secretkeyQWER1234!@#$'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=10)


@app.route("/")
def home():
    if 'username' in session:  # session안에 username이 있으면 로그인
        current_user = session['username']
        return jsonify({'session_user': current_user})

    return render_template('index.html')


@app.route("/login")
def login_page():
    return render_template('login.html')


@app.route("/login", methods=["POST"])
def do_login():
    id_receive = request.form['member_id']
    pw_receive = request.form['member_pw']

    user_id = db.members.find_one({'memberid': id_receive}, {'_id': False})
    user_pw = db.members.find_one({'memberid': id_receive, 'memberpw': pw_receive}, {'_id': False})

    if user_id is None:
        return jsonify({'msg': '존재 하지 않는 아이디 입니다'})
    elif user_pw is None:
        return jsonify({'msg': '비밀 번호가 다릅니다'})
    else:
        user_name = db.members.find_one({'memberid': id_receive}, {'_id': False})['name']
        print(session)
        session['username'] = id_receive
        return jsonify({'msg': '로그인 완료!', 'member': user_name, 'sessionid': session['username']})


@app.route("/logout", methods=["GET"])
def do_logout():
    session.pop('username', None)
    return jsonify({'msg': '세션이 종료 되었습니다!'})


@app.route("/new_member")
def new_member_page():
    return render_template('new_member.html')


@app.route("/signup", methods=["POST"])
def sign_up():
    userid_receive = request.form['userid']
    userpw_receive = request.form['userpw']
    username_receive = request.form['username']
    usernickname_receive = request.form['usernickname']

    doc = {
        'memberid': userid_receive,
        'memberpw': userpw_receive,
        'name': username_receive,
        'nickname': usernickname_receive
    }

    doc_id = doc['memberid']
    doc_nickname = doc['nickname']

    members = list(db.members.find({}, {'_id': False}))

    for mem in members:
        mem_id = mem['memberid']
        mem_nickname = mem['nickname']
        if doc_id == mem_id:
            return jsonify({'msg': '동일한 id가 존재합니다!'})
        elif doc_nickname == mem_nickname:
            return jsonify({'msg': '동일한 닉네임이 존재합니다!'})

    db.members.insert_one(doc)
    return jsonify({'msg': '회원 가입 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
