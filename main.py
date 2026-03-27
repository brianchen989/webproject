from flask import Flask,render_template, request, jsonify

from flask import request, jsonify
from openai import OpenAI#匯入openai套件

import uuid # 用來產生隨機 ID

import models # 匯入資料庫與 Event 模型
import utils.tool as tool # 匯入熱量計算工具

# 建立 Flask 應用程式
app = Flask(__name__,template_folder='static/templates',static_folder='static')

# 這裡請換成你申請到的 Google API 金鑰 (Gemini)
# 注意：程式碼要上傳到公開的 GitHub 等地方時，千萬要記得把它遮蔽或刪掉！

#genai.configure(api_key="[ENCRYPTION_KEY]")

# 初始化 Gemini 模型
# gemini-1.5-flash 是目前 Google 官方推薦既快速又聰明的模型版本
#model = genai.GenerativeModel('gemini-1.5-flash')

# 告訴 Flask 資料庫路徑與檔名（sqlite:/// 代表存在專屬的檔案裡）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'

# 關閉 SQLAlchemy 內建的追蹤功能（可以省點效能）
app.config['AIzaSyBGiGLX9fL6N-knztY17oSLYB-Z4BopWwc'] = False
# 啟動資料庫服務
models.db.init_app(app)

@app.route('/')
def index():
    title = "陳辰的網頁"
    return render_template("index.html", title=title)

@app.route('/to_do')
def to_do():
    title = "還沒做好的網頁"
    return render_template("to_do.html", title=title)

'''
@app.route("/api/chat", methods=["POST"])
def chat():
    # 1. 取得前端傳過來的資料（JSON 格式）
    data = request.get_json()
    user_message = data.get("message")
    # 如果沒收到訊息，就回傳錯誤
    if not user_message:
        return jsonify({"error": "沒有收到內容"}), 400
    try:
        # 2. 呼叫 Google Gemini API
        # 我們在這裡把「浣熊助手」的設定跟使用者的問題組合在一起
        prompt = f"你是一隻熱情、會幫忙回答問題的浣熊 AI 助手，在回答時可以加上可愛的語氣詞(例如：啾、呢、呀)。\n現在使用者的問題是：{user_message}"
        
        response = model.generate_content(prompt)
        
        # 3. 取出 AI 講的文字
        ai_reply = response.text
        
        # 4. 把文字打包成 JSON 格式還給前端
        return jsonify({"reply": ai_reply})
    except Exception as e:
        # 如果發生錯誤（例如 API key 錯誤、網路斷線等）
        print("API 發生錯誤:", e)
        return jsonify({"error": "不好意思，我的腦袋稍微卡住了，請稍後再試！"}), 500
'''
# 啟動伺服器
if __name__ == "__main__":
    # 建立資料庫
    with app.app_context():
        models.db.create_all()# 建立資料表
    app.run(debug=True,port=5000,host='0.0.0.0')