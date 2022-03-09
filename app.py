import re
from unittest import result
from flask import Flask, request, redirect, render_template, session
import json

# application 物件
app = Flask(
    __name__,
    static_folder="static", #靜態資料夾名稱
    static_url_path="/file" #靜態檔案對應路徑
)
app.secret_key = "123456789"  #使用 session 需要先設定 secret_key

@app.route("/en/")
def index_english():
    return json.dumps({
        "status":"ok",
        "text":"Hello World"              
    })

@app.route("/zh/")
def index_zh():
    return json.dumps({
        "status":"ok",
        "text":"哈囉 世界"              
    }, ensure_ascii=False)

#建立路徑 /對應路徑的處理Function
@app.route("/")
def index():
    # print("請求方法", request.method)
    # print("通訊協定", request.scheme)
    # print("主機名稱", request.host)
    # print("路徑", request.path)
    # print("完整網址", request.url)
    # print("瀏覽器和作業系統", request.headers.get("user-agent"))
    #print("語言偏好", request.headers.get("accept-language"))
    # print("引薦網址", request.headers.get("referrer"))
    lang = request.headers.get("accept-language")
    if lang.startswith("en"):
        return redirect("/en/")
    else:
        return redirect("/temp")

@app.route("/temp")
def temp():
    return render_template("index.html",name = "小明")

#使用get 方法，利用路徑 /getsum 處理對應的函式
@app.route("/getSum", methods = ["POST"])
def getSum():
    #get 方法使用 maxNum = request.args.get("max", 100) #取的 query string
    maxNum = request.form["max"]
    maxNum = int(maxNum)
    result = 0
    for n in range(1,maxNum+1):
        result+=n
    return "結果"+str(result)

#動態路由，取得網址上的字
@app.route("/user/<username>")
def handleUser(username):
    if username == "love":
        return username + " you"
    else:
        return username + " is wrong answer"

#使用 GET 方法處理路徑 /hello?name=使用者名字
@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    session["username"] = name  #session[欄位名稱] = 資料
    return "你好 "+name

@app.route("/talk")
def talk():
    name = session["username"] # 取出 session 中儲存的值
    return name + " 很高興再次見到"

#可指定 port 號碼
app.run(port=3000)


