# 패키지 설치 -> flask, pymongo, dnspython

from flask import Flask, render_template, request, jsonify, redirect
app = Flask(__name__)

app.secret_key = '1a2ss3ddd'

from pymongo import MongoClient
client = MongoClient('mongodb+srv://ahn:sparta@cluster0.s9tldtb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbprestudy

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    # GET 방식이면 페이지 이동
    if request.method == 'GET':
        return render_template('login.html')
    else:
        memberId = request.form['member_id']
        memberPw = request.form['member_pw']

        print(memberId, memberPw)

        member = db.member.find_one({'memberId': request.form['member_id']})

        print(member)


        # POST 방식이면 ID 먼저 확인
        if db.member.find_one({'memberId': request.form['member_id']}) is None:
            return jsonify({'msg': '일치하는 아이디가 없습니다!'})
        else:
            pwd = db.member.find_one({'memberId': request.form['member_id']})["memberPw"]
            # 잁치하는 ID가 존재할 경우 비밀번호 조회
            if request.form['member_pw'] == pwd:
                return jsonify({'msg': '로그인 완료!'})
            else:
                return jsonify({'msg': '비밀번호가 일치하지 않습니다!'})

@app.route("/logout")
def doLogOut():
    return jsonify({'msg': 'POST 연결 완료!'})

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