from flask import Flask,render_template, request, jsonify

import google.generativeai as genai

import uuid # 用來產生隨機 ID

import models # 匯入資料庫與 Event 模型
import utils.tool as tool # 匯入熱量計算工具

# 建立 Flask 應用程式
app = Flask(__name__,template_folder='static/templates',static_folder='static')

# ==========================================
# [AI 助手功能區塊設定]
# 這裡負責設定 Google 的 Gemini AI 模型
# ==========================================
# 透過 google.generativeai 呼叫 Google AI 服務
# 這裡請換成你申請到的 Google API 金鑰 (Gemini)
# 注意：程式碼要上傳到公開的 GitHub 等地方時，千萬要記得把它遮蔽或刪掉！
genai.configure(api_key="[ENCRYPTION_KEY]")

# 初始化 Gemini 模型
# 這裡指定使用 gemini-2.5-flash，負責處理前端 (網2.0.js) 傳來的聊天文字
# 這是目前 Google 官方推薦既快速又聰明的模型版本
model = genai.GenerativeModel('gemini-2.5-flash')

# 告訴 Flask 改用 Supabase 雲端資料庫 (PostgreSQL)
# ⚠️ 注意：請把下面的引號內的網址，換成你在 Supabase 上取得的真實 Database URL
# 格式大約會長得像這樣： 'postgresql://postgres.xxxxxx:你的密碼@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.vcqtfeqthtdwwxzgmdfj:fZH_stpyw886NMq@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres'

# 關閉 SQLAlchemy 內建的追蹤功能（可以省點效能）
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

@app.route('/quiz.html')
def quiz():
    title = "知識大挑戰"
    return render_template("quiz.html", title=title)

@app.route('/goal_<int:goal_id>')
def goal(goal_id):
    title = f"SDGs 目標 {goal_id}"
    return render_template(f"goal_{goal_id}.html", title=title)

# ==========================================
# [AI 助手後端對話路由]
# 負責接收前端的訊息，並將回應用 JSON 傳回前端
# 交互檔案： 
# - 前端 HTML: static/templates/index.html (包含使用者介面：對話視窗)
# - 前端 JS: static/js/網2.0.js (透過其中 fetch() 功能發送 POST 請求到這個路由)
# ==========================================
@app.route("/api/chat", methods=["POST"])
def chat():
    # 1. 取得前端 (網2.0.js) 透過 fetch 方法傳過來的 JSON 格式資料
    # 資料格式預期為：{"message": "在此填入使用者的文字"}
    data = request.get_json()
    user_message = data.get("message")
    
    # 防呆機制：如果沒有收到訊息，就回傳 400 錯誤代碼與錯誤訊息給前端
    if not user_message:
        return jsonify({"error": "沒有收到內容"}), 400
        
    try:
        # 2. 設計 Prompt (提示詞) 並呼叫 Google Gemini API
        # 這裡會把「浣熊助手」的特徵設定與使用者的實際問題組合起來一起交給 AI 模型
        prompt = f"你是一隻熱情、會幫忙回答問題的浣熊 AI 助手，在回答時可以加上可愛的語氣詞(例如：啾、呢、呀)。\n現在使用者的問題是：{user_message}"
        
        # 呼叫模型，並請它根據上方的 Prompt 去產生回應文字
        response = model.generate_content(prompt)
        
        # 3. 取得 AI 成功回覆的文字內容
        ai_reply = response.text
        
        # 4. 把文字打包成 JSON 格式還給前端 (網2.0.js 會接收此資料，並顯示在使用者畫面上)
        # 回傳格式範例：{"reply": "你好呀！我是浣熊助手啾！"}
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        # 5. 錯誤處理 (發生例如 API 金鑰錯誤、網路斷線、模型錯誤等突發狀況)
        # 這裡會印出真實錯誤到伺服器的終端機畫面，方便開發者進行除錯
        print("API 發生錯誤:", e)
        # 丟出一個比較平易近人的備用訊息還給前端，避免出現亂碼或讓網頁當機
        return jsonify({"error": "不好意思，我的腦袋稍微卡住了，請稍後再試！"}), 500
# ==========================================
# [排行榜相關 API]
# ==========================================
@app.route("/api/submit_score", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")
    
    if not name or score is None:
        return jsonify({"error": "請提供暱稱與分數"}), 400
        
    try:
        new_record = models.PlayerScore(name=name, score=score)
        models.db.session.add(new_record)
        models.db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print("資料庫儲存錯誤:", e)
        return jsonify({"error": "儲存失敗"}), 500

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        # 取出前 10 名（分數由高到低，分數相同則依時間先後）
        top_scores = models.PlayerScore.query.order_by(
            models.PlayerScore.score.desc(), 
            models.PlayerScore.created_at.asc()
        ).limit(10).all()
        return jsonify([s.to_dict() for s in top_scores])
    except Exception as e:
        print("讀取排行榜錯誤:", e)
        return jsonify({"error": "讀取失敗"}), 500

def init_mini_games():
    # 檢查是否已經記錄了 quiz
    quiz_game = models.MiniGame.query.filter_by(game_name="quiz").first()
    if not quiz_game:
        # 新增 quiz 並將 17 個目標都設為 True (因為知識大挑戰涵蓋所有領域)
        new_quiz = models.MiniGame(
            game_name="quiz",
            file_path="quiz.html",
            description="涵蓋全部 ESG 與 SDGs 知識的綜合大挑戰",
            goal_1=True, goal_2=True, goal_3=True, goal_4=True, goal_5=True,
            goal_6=True, goal_7=True, goal_8=True, goal_9=True, goal_10=True,
            goal_11=True, goal_12=True, goal_13=True, goal_14=True, goal_15=True,
            goal_16=True, goal_17=True
        )
        models.db.session.add(new_quiz)
        models.db.session.commit()
        print("✅ 已將 quiz.html 註冊至小遊戲資料庫！")

# 啟動伺服器
if __name__ == "__main__":
    # 建立資料庫
    with app.app_context():
        models.db.create_all()# 建立資料表
        init_mini_games()     # 初始化小遊戲資料庫紀錄
    app.run(debug=True,port=5000,host='0.0.0.0')