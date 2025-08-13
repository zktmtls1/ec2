#하만 2 폴더 - server 폴더 - exam01.py
# response : 서버->클라이언트
# request : 클라이언트 ->서버


#파이썬 서버
#1) flask: 마이크로 웹 프레임워크
#2) Django: 보안 등 모안 기능이 포함됨. flask에 비해 10배 무겁

from flask import Flask, render_template, request, redirect, make_response #### 

from aws import detect_labels_local_file
from aws import compare_faces as cf
from werkzeug.utils import secure_filename

import os 
# static 폴더 없다면 생성
if not os.path.exists("static"):
    os.mkdir("static")


app = Flask(__name__)
@app.route("/") ##### 웹사이트까지 가능 경로 
def index():
    return render_template("index.html") #html 문서 로드



@app.route("/compare", methods=["POST"])
def compare_faces():

    # /detect를 통해서 한 내용과 거의 동일
    # file을 2개 받을 뿐
    # 1. compare로 오는 file1, file2를 받아서
    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]

        file1_filename = secure_filename(file1.filename)
        file2_filename = secure_filename(file2.filename)

        file1.save("static/" + file1_filename)
        file2.save("static/" + file2_filename)

        # static폴더에 save
        # 이 때, secure_filename 사용해서
        # 2. aws.py 얼굴 비교 aws 코드!!
        # 이 결과를 통해 웹 페이지에
        # "동일 인물일 확률은 95.34%입니다."
        # 3. aws.py안에 함수를 불러와서
        # exam01.py 사용!!

        r = cf("static/" + file1_filename, "static/" + file2_filename)

    return r





@app.route("/detect", methods = ["POST"])
def detect_label():
    #file이름을 secure 처리
    if request.method =="POST":
        file = request.files["file"] # 파일을 static 폴더에 저장, 경로를 detect_lo~ 함수에 전달
        file_name = secure_filename(file.filename)
        file.save("./static/" + file_name)
        r = detect_labels_local_file("./static/" + file_name)
    return r

@app.route("/secret", methods=["POST"])
def box():
    try:
        if request.method =="POST":
            #get으로 오는 데이터 ->arg[key]
            #post로 오는 데이터 ->form[key]
            hidden = request.form["hidden"]
            return f"비밀정보: {hidden}"
    except:
        return "데이터 전송 실패"

@app.route("/login", methods= ["GET"])
def login():
    if request.method =="GET":
        login_id = request.args["login_id"]
        login_pw = request.args["login_pw"]
        if login_id =="123" and login_pw =="qwe":
            response = make_response(redirect("/login/success"))
            response.set_cookie("user", login_id)
            return response
        else:  
            return redirect("/")
    return "로그인 성공"

@app.route("/login/success", methods=["GET"])
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"

if __name__=="__main__":
    app.run(host="0.0.0.0")