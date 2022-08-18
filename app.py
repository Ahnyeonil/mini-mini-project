# 패키지 설치 -> flask, pymongo, dnspython

from flask import Flask, render_template, request, jsonify, redirect, session
from datetime import timedelta

app = Flask(__name__)

# secret_key는 서버상에 동작하는 어플리케이션 구분
app.secret_key = b'1a2ss3ddd'
# 로그인 지속시간
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://ahn:sparta@cluster0.s9tldtb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbprestudy

@app.route("/")
def home():
    # session안에 memberId 존재 확인
    if 'member_id' in session:
        # loginMember 에 담기
        loginMember = session

        return render_template('main.html', loginMember=loginMember)

    return render_template('index.html')

@app.route("/main")
def main():
    return render_template('main.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    # GET 방식이면 페이지 이동
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # POST 방식이면 ID 먼저 확인
        if db.member.find_one({'memberId': request.form['member_id']}) is None:
            return jsonify({'msg': '일치하는 아이디가 없습니다!'})
        else:
            loginMemberInfo = db.member.find_one({'memberId': request.form['member_id']})
            pwd = loginMemberInfo["memberPw"]
            # 일치하는 ID가 존재할 경우 비밀번호 조회
            if request.form['member_pw'] == pwd:
                # session 추가
                session['member_id'] = request.form['member_id']
                session['mid'] = loginMemberInfo['id']

                loginMember = session

                return render_template('/main.html', loginMember=loginMember)
                # return jsonify({'msg': '로그인 완료!'})
            else:
                return jsonify({'msg': '비밀번호가 일치하지 않습니다!'})

@app.route("/logout")
def doLogOut():
    session.pop('member_id', None)
    session.pop('mid', None)
    return render_template('index.html')

@app.route("/new_member", methods=["POST", "GET"])
def newMember():
    # GET 방식이면 페이지 이동
    if request.method == 'GET':
        return render_template('new_member.html')
    else:
        print("---------- 회원가입 Start ----------")

        # 회원 Id를 위해 새로운 Collection 추가
        # 새로운 Collection 의 길이로 회원 Id 활용
        # Update 및 Delete 에 활용 가능
        memberSequence = len(list(db.memberSequence.find({})))
        db.memberSequence.insert_one({'count': memberSequence})

        memberId = request.form['member_id']
        memberPw = request.form['member_pw']
        memberName = request.form['member_name']
        memberNickname = request.form['member_nickname']

        doc = {
            'id' : memberSequence,
            'memberId': memberId,
            'memberPw': memberPw,
            'memberName': memberName,
            'memberNickname': memberNickname,
            'useYn' : "Y"
        }
        db.member.insert_one(doc)

        print("---------- 회원가입 End ----------")
        return jsonify({'msg': '회원가입이 완료되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)