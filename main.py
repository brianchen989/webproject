from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import uuid
import models
import utils.tool as tool

# 建立 Flask 應用程式
app = Flask(__name__, template_folder='static/templates', static_folder='static')

# ==========================================
# AI 助手功能設定 (Google Gemini)
# ==========================================
# 填入 Google API 金鑰 (請注意不要外洩至公開平台)
genai.configure(api_key="[ENCRYPTION_KEY]")

# 初始化 Gemini 模型 (負責處理聊天對話)
model = genai.GenerativeModel('gemini-2.5-flash')

# 設定 Supabase 雲端資料庫 (PostgreSQL) 連線字串
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.vcqtfeqthtdwwxzgmdfj:fZH_stpyw886NMq@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 綁定資料庫服務
models.db.init_app(app)

@app.route('/')
def index():
    return render_template("index.html", title="陳辰的網頁")

@app.route('/to_do')
def to_do():
    return render_template("to_do.html", title="還沒做好的網頁")

@app.route('/quiz.html')
def quiz():
    # 查詢資料庫中名為 quiz 的小遊戲屬性
    game_record = models.MiniGame.query.filter_by(game_name="quiz").first()
    active_goals = []
    
    if game_record:
        # 檢查 1 到 17 的目標，如果為 True 就加入到列表中
        for i in range(1, 18):
            if getattr(game_record, f"goal_{i}", False):
                active_goals.append(i)
                
    return render_template("quiz.html", title="知識大挑戰", active_goals=active_goals)

@app.route('/goal_<int:goal_id>')
def goal(goal_id):
    # 尋找有涵蓋此目標的小遊戲
    games = []
    try:
        all_games = models.MiniGame.query.all()
        for g in all_games:
            if getattr(g, f'goal_{goal_id}', False):
                games.append(g)
    except Exception as e:
        print(f"資料庫查詢遊戲失敗: {e}")
        
    return render_template(f"goal_{goal_id}.html", title=f"SDGs 目標 {goal_id}", games=games)

# ==========================================
# AI 助手對話 API
# ==========================================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    
    # 檢查是否包含訊息內容
    if not user_message:
        return jsonify({"error": "沒有收到內容"}), 400
        
    try:
        # 設定 AI 角色與提示詞
        prompt = f"你是一隻熱情、會幫忙回答問題的浣熊 AI 助手，在回答時可以加上可愛的語氣詞(例如：啾、呢、呀)。\n現在使用者的問題是：{user_message}"
        response = model.generate_content(prompt)
        
        # 回傳 AI 回應至前端
        return jsonify({"reply": response.text})
        
    except Exception as e:
        # 錯誤處理與日誌記錄
        print("API 發生錯誤:", e)
        return jsonify({"error": "不好意思，我的腦袋稍微卡住了，請稍後再試！"}), 500

# ==========================================
# 排行榜相關 API
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
    # 檢查資料庫是否已記錄 quiz 遊戲
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
    with app.app_context():
        models.db.create_all() # 建立資料表
        init_mini_games()      # 初始化小遊戲資料庫紀錄
    app.run(debug=True, port=5000, host='0.0.0.0')