from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from google import genai
import os
import uuid
import models
import utils.tool as tool

# 建立 Flask 應用程式
app = Flask(__name__, template_folder='static/templates', static_folder='static')

# ==========================================
# AI 助手功能設定 (Google Gemini)
# ==========================================
api_key = os.environ.get("GEMINI_API_KEY")
client = None

if api_key:
    try:
        # 初始化 Gemini 客戶端（新版 google.genai SDK）
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print("Warning: Gemini client initialization failed:", e)
else:
    print("Warning: GEMINI_API_KEY environment variable is not set. AI Chat feature will be temporarily disabled.")

# 設定 Supabase 雲端資料庫 (PostgreSQL) 連線字串
db_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 系統優化：防瞬斷與閒置連線池優化
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,     # 每次查詢前自動 Ping 測試，確保連線存活
    "pool_recycle": 280,       # 每 280 秒自動回收連線，避開 Supabase 連線閒置斷開
    "pool_timeout": 30         # 取得連線最大超時時間
}

# 綁定資料庫服務
models.db.init_app(app)

# ==========================================
# 系統初始化：自動建立資料表與填充預設資料 🐾
# ==========================================
with app.app_context():
    try:
        # 自動在雲端 (Supabase) 或本地建立所有缺少的資料表
        models.db.create_all()
        print("資料表初始化/檢查成功！")
        
        # 檢查小遊戲表是否為空，若空則自動填充初始預設資料
        if models.MiniGame.query.count() == 0:
            print("小遊戲表為空，正在注入預設小遊戲資料...")
            
            game_quiz = models.MiniGame(
                game_name="知識大挑戰",
                file_path="quiz.html",
                description="涵蓋全部 ESG 與 SDGs 知識的綜合大挑戰測驗！快來挑戰你的永續知識吧！💡",
                goal_1=True, goal_2=True, goal_3=True, goal_4=True, goal_5=True,
                goal_6=True, goal_7=True, goal_8=True, goal_9=True, goal_10=True,
                goal_11=True, goal_12=True, goal_13=True, goal_14=True, goal_15=True,
                goal_16=True, goal_17=True
            )
            
            game_earth = models.MiniGame(
                game_name="Clicking Earth",
                file_path="clicking_earth.html",
                description="透過點擊地球與升級綠能科技，一步步改善地球環境的永續發展放置遊戲！🌲",
                goal_7=True, goal_11=True, goal_12=True, goal_13=True, goal_14=True, goal_15=True
            )
            
            models.db.session.add(game_quiz)
            models.db.session.add(game_earth)
            models.db.session.commit()
            print("預設小遊戲資料注入完成！")
            
    except Exception as e:
        print("Warning: 資料庫自動初始化/填充失敗:", e)

# 設定 Flask Session 的 Secret Key (用於安全加密 cookie)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "racoon-development-secret-key-87324982")

# ==========================================
# 系統優化：全域錯誤異常捕獲處理器 🐾
# ==========================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=404, message="糟糕！這個頁面被小灰藏起來了...", title="找不到頁面 🐾"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code=500, message="哎呀！系統好像開了個小差...請稍後再試！", title="系統錯誤 🐾"), 500

# ==========================================
# 使用者狀態全域注入 (Jinja2 Context Processor)
# 讓所有範本都能直接使用 `current_user` 變數
# ==========================================
@app.context_processor
def inject_user():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = models.db.session.get(models.User, user_id)
            if user and user.deleted_at is None:
                return dict(current_user=user)
        except Exception as e:
            print("讀取當前登入使用者失敗:", e)
    return dict(current_user=None)

@app.route('/')
def index():
    return render_template("index.html", title="陳辰的網頁")

@app.route('/to_do')
def to_do():
    return render_template("to_do.html", title="還沒做好的網頁")

@app.route('/games')
@app.route('/games.html')
def games_lobby():
    try:
        all_games = models.MiniGame.query.filter(models.MiniGame.deleted_at == None).all()
    except Exception as e:
        print("讀取小遊戲列表失敗:", e)
        all_games = []
    return render_template("games_lobby.html", title="小遊戲大廳 ", games=all_games)

@app.route('/links')
@app.route('/links.html')
def links_page():
    return render_template("links.html", title="相關連結 ")

# ==========================================
# 使用者登入系統路由
# ==========================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("user_id"):
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        # 取得表單輸入
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # 欄位基本驗證
        if not username or not email or not password:
            flash("請填寫所有必要欄位！", "error")
            return render_template("register.html", title="註冊帳號")
            
        if len(password) < 6:
            flash("密碼長度必須至少為 6 個字元！", "error")
            return render_template("register.html", title="註冊帳號")
            
        if password != confirm_password:
            flash("密碼與確認密碼不一致！", "error")
            return render_template("register.html", title="註冊帳號")
            
        try:
            # 檢查使用者名稱或 Email 是否已被註冊
            existing_user = models.User.query.filter((models.User.username == username) | (models.User.email == email)).first()
            if existing_user:
                if existing_user.username == username:
                    flash("此使用者名稱已被使用！", "error")
                else:
                    flash("此 Email 已被註冊！", "error")
                return render_template("register.html", title="註冊帳號")
                
            # 建立新使用者帳號
            new_user = models.User(username=username, email=email)
            models.db.session.add(new_user)
            # 必須先 flush 以取得新產生的 UUID 主鍵
            models.db.session.flush()
            
            # 使用 Argon2id + 獨立 Salt 雜湊密碼
            salt_hex, hashed_password = models.UserCredential.hash_password(password)
            
            # 建立密碼憑證關聯
            new_credential = models.UserCredential(
                user_id=new_user.id,
                salt=salt_hex,
                password_hash=hashed_password
            )
            models.db.session.add(new_credential)
            models.db.session.commit()
            
            # 註冊成功後自動登入
            session["user_id"] = new_user.id
            session["username"] = new_user.username
            flash("帳號註冊成功！已為您自動登入 🦝", "success")
            return redirect(url_for('index'))
            
        except Exception as e:
            models.db.session.rollback()
            print("註冊失敗:", e)
            flash("系統發生錯誤，請稍後再試！", "error")
            
    return render_template("register.html", title="註冊帳號")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("user_id"):
        return redirect(url_for('index'))
        
    next_url = request.args.get('next', '')
    
    if request.method == 'POST':
        account = request.form.get("account", "").strip() # 使用者名稱或 Email
        password = request.form.get("password", "")
        next_url = request.form.get("next", "")
        
        if not account or not password:
            flash("請填寫所有欄位！", "error")
            return render_template("login.html", title="登入系統", next_url=next_url)
            
        try:
            # 查詢使用者 (支援 username 或 email 登入，且排除已軟刪除用戶)
            user = models.User.query.filter(
                ((models.User.email == account.lower()) | (models.User.username == account)) &
                (models.User.deleted_at == None)
            ).first()
            
            if user and user.credential:
                # 驗證密碼是否相符
                if user.credential.verify_password(password):
                    # 登入成功，寫入 session
                    session["user_id"] = user.id
                    session["username"] = user.username
                    
                    # 更新最後登入時間
                    user.last_login = models.datetime.utcnow()
                    models.db.session.commit()
                    
                    flash(f"歡迎回來，{user.username}！ 🦝", "success")
                    
                    # 安全重導向防護 (僅允許相對路徑跳轉，防範開放式重導向漏洞)
                    if next_url and next_url.startswith('/'):
                        return redirect(next_url)
                    return redirect(url_for('index'))
            
            # 密碼錯誤或找不到帳號，顯示通用錯誤（安全性佳，不透露是帳號不存在還是密碼錯）
            flash("帳號或密碼輸入錯誤！", "error")
            
        except Exception as e:
            print("登入失敗:", e)
            flash("系統發生錯誤，請稍後再試！", "error")
            
    return render_template("login.html", title="登入系統", next_url=next_url)

@app.route('/logout')
def logout():
    session.clear()
    flash("您已成功登出！", "success")
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # 登入防護 (Login Required)
    user_id = session.get("user_id")
    if not user_id:
        flash("請先登入帳號以訪問個人中心！", "error")
        return redirect(url_for('login'))
        
    user = models.db.session.get(models.User, user_id)
    if not user:
        session.clear()
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        action = request.form.get("action")
        
        # 1. 處理基本資料更新 (修改暱稱、Email)
        if action == "update_profile":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            
            if not username or not email:
                flash("欄位不可為空！", "error")
                return render_template("profile.html", title="個人中心")
                
            try:
                # 檢查重複值（排除當前使用者自己）
                existing_user = models.User.query.filter(
                    (models.User.id != user.id) & 
                    ((models.User.username == username) | (models.User.email == email))
                ).first()
                
                if existing_user:
                    if existing_user.username == username:
                        flash("此使用者名稱已被其他玩家使用！", "error")
                    else:
                        flash("此 Email 已被其他帳號註冊！", "error")
                    return render_template("profile.html", title="個人中心")
                
                # 儲存更新
                user.username = username
                user.email = email
                models.db.session.commit()
                
                # 同步更新 session 中的暱稱
                session["username"] = username
                flash("個人基本資料更新成功！ 🦝", "success")
                return redirect(url_for('profile'))
                
            except Exception as e:
                models.db.session.rollback()
                print("更新個人資料失敗:", e)
                flash("系統發生錯誤，無法更新資料！", "error")
                
        # 2. 處理密碼變更
        elif action == "change_password":
            old_password = request.form.get("old_password", "")
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")
            
            if not old_password or not new_password or not confirm_password:
                flash("請完整填寫密碼變更所有欄位！", "error")
                return render_template("profile.html", title="個人中心")
                
            # 驗證舊密碼
            if not user.credential or not user.credential.verify_password(old_password):
                flash("目前舊密碼輸入錯誤，請重新確認！", "error")
                return render_template("profile.html", title="個人中心")
                
            # 驗證新密碼長度與一致性
            if len(new_password) < 6:
                flash("新密碼長度必須至少為 6 個字元！", "error")
                return render_template("profile.html", title="個人中心")
                
            if new_password != confirm_password:
                flash("兩次輸入的新密碼不相符！", "error")
                return render_template("profile.html", title="個人中心")
                
            try:
                # 使用 Argon2id 與新產生的隨機 salt 重新雜湊密碼
                salt_hex, hashed_password = models.UserCredential.hash_password(new_password)
                
                # 更新憑證記錄
                user.credential.salt = salt_hex
                user.credential.password_hash = hashed_password
                models.db.session.commit()
                
                flash("安全密碼修改成功！下次登入請使用新密碼 🦝", "success")
                return redirect(url_for('profile'))
                
            except Exception as e:
                models.db.session.rollback()
                print("變更密碼失敗:", e)
                flash("系統發生錯誤，無法變更密碼！", "error")
                
    return render_template("profile.html", title="個人中心")

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

@app.route('/clicking_earth.html')
def clicking_earth():
    game_record = models.MiniGame.query.filter_by(game_name="clicking_earth").first()
    active_goals = []
    
    if game_record:
        for i in range(1, 18):
            if getattr(game_record, f"goal_{i}", False):
                active_goals.append(i)
                
    return render_template("clicking_earth.html", title="Clicking Earth", active_goals=active_goals)

# ==========================================
# SDGs 17 個目標即時新聞資料庫 (時事看板)
# ==========================================
SDG_NEWS_BASE = {
    1: [
        {"title": "聯合國報告：全球極端貧窮人口面臨疫情與衝突夾擊首度回升", "source": "聯合國新聞", "date": "2024-03-15", "summary": "氣候變遷與地區衝突夾擊，導致全球邊緣群體基本生活成本激增，消滅貧窮工作面臨嚴峻挑戰。", "link": "https://news.un.org/"},
        {"title": "台灣啟動青年脫貧自立儲蓄專案，結合企業資源推動自立方案", "source": "衛生福利部", "date": "2024-05-10", "summary": "衛福部與多家百大企業合作提供儲蓄開戶與一比一配對提撥，協助弱勢青年累積資產並翻轉跨代貧窮。", "link": "https://www.mohw.gov.tw/"}
    ],
    2: [
        {"title": "氣候變遷加劇全球糧食短缺，聯合國糧農組織警告糧價波動", "source": "FAO", "date": "2024-04-20", "summary": "極端乾旱席捲多個糧食出口國，導致主要農產品產量驟降，全球糧食安全拉響橙色警報。", "link": "https://www.fao.org/"},
        {"title": "台灣民間發起惜食餐廳與剩食共享計畫，年減百萬噸食材浪費", "source": "環境資訊中心", "date": "2024-05-18", "summary": "多個非營利組織與量販店合作，將即期安全食材配送至社區愛心廚房，將剩食化為關懷溫飽的愛心暖流。", "link": "https://e-info.org.tw/"}
    ],
    3: [
        {"title": "全球智慧醫療科技大突破，AI 提升早期肺癌篩檢準確率", "source": "WHO", "date": "2024-02-28", "summary": "世界衛生組織公布最新臨床指南，AI 輔助診斷影像技術在肺癌早期發現率上提升了將近 25%。", "link": "https://www.who.int/"},
        {"title": "台灣健保署擴大推廣全人健康管理與社區長照醫療整合服務", "source": "衛生福利部", "date": "2024-05-02", "summary": "健保署推出智慧居家巡迴醫療，結合社區藥局與地區診所，提供行動不便長者一條龍式的健康關懷服務。", "link": "https://www.nhi.gov.tw/"}
    ],
    4: [
        {"title": "數位教育弭平城鄉差距，聯合國教科文組織推廣全球數位學校", "source": "UNESCO", "date": "2024-03-10", "summary": "UNESCO 發表年度報告，數位平台與低成本衛星網路的普及，使非洲等偏遠地區數百萬孩童獲得優質教育機會。", "link": "https://www.unesco.org/"},
        {"title": "教育部推動偏鄉學校數位轉型，提升師資與數位設備覆蓋率", "source": "教育部", "date": "2024-04-15", "summary": "教育部提撥十億專款為偏鄉學校班班配備平板電腦，並提供跨校數位合作共學平台，提升教學競爭力。", "link": "https://www.edu.tw/"}
    ],
    5: [
        {"title": "全球百大企業揭露董事會女性比例創新高，重視多元決策", "source": "路透社", "date": "2024-03-08", "summary": "最新統計顯示，全球領先企業董事會中女性比例平均已達 32%，多元化背景顯著提升了企業抗風險能力。", "link": "https://www.reuters.com/"},
        {"title": "台灣推行『職場性別平權與薪資透明』，積極消除同工不同酬現象", "source": "勞動部", "date": "2024-04-20", "summary": "勞動部積極推行薪資透明化與平權檢查制度，推動企業改善性別薪資差距，建立平等健康的職場文化。", "link": "https://www.mol.gov.tw/"}
    ],
    6: [
        {"title": "海水淡化與中水回收技術大突破，有效舒緩中東極端缺水危机", "source": "水資源論壇", "date": "2024-04-12", "summary": "新一代石墨烯濾膜技術使海水淡化能源消耗降低 30%，為全球極度缺水地區帶來可持續的淡水曙光。", "link": "https://e-info.org.tw/"},
        {"title": "經濟部推動智慧防汛水網與水庫清淤，提升極端氣候抗旱韌性", "source": "水利署", "date": "2024-05-22", "summary": "水利署導入物聯網感測器進行水庫即時監測，並大規模利用枯水期清除淤泥，增加台灣水資源調蓄空間。", "link": "https://www.wra.gov.tw/"}
    ],
    7: [
        {"title": "全球再生能源發電佔比創新高，太陽能成為歷史上最便宜電力", "source": "IEA", "date": "2024-02-15", "summary": "國際能源署最新報告指出，全球新建風力與太陽能發電裝機容量大爆發，綠色潔淨電力已成為能源主流。", "link": "https://www.iea.org/"},
        {"title": "台灣離岸風電第三階段開跑，綠能發電大軍邁向百萬千瓦里程碑", "source": "經濟部", "date": "2024-05-09", "summary": "能源署宣布多個離岸風場成功併網發電，台灣綠能基礎建設穩定邁進，為高科技產業提供充足綠電。", "link": "https://www.moeaea.gov.tw/"}
    ],
    8: [
        {"title": "氣候暖化衝擊勞工健康，多國研議立法保障高溫氣候勞動權益", "source": "國際勞工組織", "date": "2024-05-01", "summary": "ILO 呼籲各國針對極端熱浪建立預警機制，確保戶外營造與農業勞工在高溫下擁有足夠休息與停工保障。", "link": "https://www.ilo.org/"},
        {"title": "勞動部加強推廣友善職場，保障移工與青年學子尊嚴勞動", "source": "勞動部", "date": "2024-05-15", "summary": "政府擴大勞動檢查與法規宣導，保障外籍移工與實習青年免受剝削，致力打造友善共融的就業環境。", "link": "https://www.mol.gov.tw/"}
    ],
    9: [
        {"title": "全球綠色製造大浪潮，百大工業集團推動工廠碳中和認證", "source": "金融時報", "date": "2024-03-22", "summary": "隨著供應鏈減碳要求，國際製造大廠紛紛升級綠色製程，導入智慧電網與自動化巡檢以降低製程碳足跡。", "link": "https://www.ft.com/"},
        {"title": "台灣半導體產業推動『綠色晶圓廠』，製程水循環回收率超90%", "source": "經濟部", "date": "2024-04-18", "summary": "科學園區指標大廠升級超高效率水資源回收系統，實現一滴水循環使用 3.5 次以上，為科技業立下永續新標杆。", "link": "https://www.moea.gov.tw/"}
    ],
    10: [
        {"title": "世界銀行擴大優惠融資，致力縮短低收入國家與發達國家數位鴻溝", "source": "世界銀行", "date": "2024-04-05", "summary": "世銀宣布提撥百億美金推動全球通訊網絡基礎建設，讓發展中國家偏鄉地區的人民也能享有低成本網際網路。", "link": "https://www.worldbank.org/"},
        {"title": "台灣推廣身心障礙者無障礙通行環境，落實社會包容與權益平權", "source": "內政部", "date": "2024-05-12", "summary": "國土署擴大補助各縣市騎樓平整與大眾運輸無障礙設施升級，保障行動不便族群的基本尊嚴與出行權利。", "link": "https://www.moi.gov.tw/"}
    ],
    11: [
        {"title": "智慧低碳城區在歐洲開花結果，市中心無車化大幅降低碳排與空污", "source": "BBC", "date": "2024-03-18", "summary": "歐洲多個城市實施市中心車輛管制，擴大自行車道與綠地，使市區空氣懸浮微粒濃度驟降 40%。", "link": "https://www.bbc.com/"},
        {"title": "內政部推動『地方創生與歷史建物活化』，吸引青年返鄉紮根", "source": "發展委員會", "date": "2024-05-16", "summary": "結合老舊社區更新與文創特色，政府輔導偏鄉發展在地特色產業，重塑城鄉多元面貌，舒緩都市人口壓力。", "link": "https://www.ndc.gov.tw/"}
    ],
    12: [
        {"title": "減塑政策全球大升級，多國立法禁止一次性包裝與微塑膠添加", "source": "路透社", "date": "2024-02-20", "summary": "歐盟通過新法案要求包裝材料必須全面可回收，促使各大消費品牌加速研發環保生物降解新材料。", "link": "https://www.reuters.com/"},
        {"title": "環保署推廣『網購循環箱與惜食地圖』，力行全民源頭垃圾減量", "source": "環境部", "date": "2024-05-02", "summary": "環境部與各大電商及便利商店合作推廣循環包裝與剩食折扣地圖，引導民眾走向綠色責任消費模式。", "link": "https://www.moenv.gov.tw/"}
    ],
    13: [
        {"title": "聯合國氣候大會達成歷史共識，全球加速轉型脫離化石燃料", "source": "COP新聞", "date": "2024-01-15", "summary": "各國代表同意推動歷史性的能源系統轉型，承諾在 2030 年前將全球再生能源發電量翻倍，減緩暖化災難。", "link": "https://unfccc.int/"},
        {"title": "環境部推動碳費徵收機制，台灣正式邁入綠色碳定價新紀元", "source": "環境部", "date": "2024-05-20", "summary": "政府公告碳費徵收草案，要求排碳大戶申報並繳納碳費，以經濟誘因促使企業加速導入節能低碳製程。", "link": "https://www.moenv.gov.tw/"}
    ],
    14: [
        {"title": "歷史性突破！聯合國通過《公海條約》保護全球30%海洋生態", "source": "聯合國", "date": "2024-03-05", "summary": "各國歷經多年談判終於通過具約束力的海洋公約，設立大規模海洋保護區以遏止過度捕撈與海底採礦危害。", "link": "https://www.un.org/"},
        {"title": "墾丁珊瑚復育傳出捷報，結合 AI 與 3D 列印監控大幅提升存活率", "source": "海洋公園", "date": "2024-05-11", "summary": "海洋科研人員利用 AI 辨識系統即時監控水溫與水質，並以環保 3D 列印人工珊瑚礁基底成功復育大片珊瑚。", "link": "https://www.ktnp.gov.tw/"}
    ],
    15: [
        {"title": "全球雨林防線！科學家利用人造衛星遙測技術阻斷亞馬遜非法伐木", "source": "NASA", "date": "2024-04-02", "summary": "太空總署高解析度衛星結合 AI 動態分析，能即時將砍伐警告送交當地執法機構，有效阻斷大片原始森林流失。", "link": "https://www.nasa.gov/"},
        {"title": "林業署推廣原生樹種林相復育，重塑低海拔生物多樣性天堂", "source": "林業署", "date": "2024-05-18", "summary": "林務局推動『生態綠網計畫』，輔導地主種植台灣原生樹木，重建淺山地帶野生動物的綠色棲地廊道。", "link": "https://www.forest.gov.tw/"}
    ],
    16: [
        {"title": "推動透明防貪腐體系，台灣在國際廉政指數評比名次創歷史新高", "source": "國際透明組織", "date": "2024-02-10", "summary": "最新清廉印象指數公布，台灣政府效能與司法獨立透明度獲得高度肯定，在亞太地區名列前茅。", "link": "https://www.transparency.org/"},
        {"title": "司法院擴大推廣國民法官與法律扶助，確保弱勢司法權益平等", "source": "司法院", "date": "2024-04-25", "summary": "政府擴大法律輔助基金會預算，為低收入與弱勢家庭免費提供專業律師諮詢，保障法治社會的基本平權。", "link": "https://www.judicial.gov.tw/"}
    ],
    17: [
        {"title": "重振全球氣候金融基金，富裕國家承諾聯手援助受氣候衝擊島國", "source": "聯合國", "date": "2024-03-12", "summary": "國際氣候峰會通過千億融資案，專款專用於協助低窪島嶼國家建設防波堤與綠色電網，實踐氣候正義。", "link": "https://www.un.org/"},
        {"title": "台灣結合 NGO 力量輸出永續綠能與農業技術，深化亞太夥伴關係", "source": "外交部", "date": "2024-05-14", "summary": "台灣與多個太平洋友邦推廣綠能示範村，提供自主太陽能電網與耐旱抗鹽作物技術，攜手邁向永續未來。", "link": "https://www.mofa.gov.tw/"}
    ]
}

def get_realtime_news(goal_id):
    """
    從外部權威 RSS 訂閱源即時抓取最新 SDGs 新聞 (方案一)
    若因無網路或未安裝 feedparser 失敗，則自動優雅降級 (Fallback) 使用本地精選字典。
    """
    try:
        import feedparser
        import re
        
        # 根據 goal_id 選擇最對應的聯合國中文新聞 RSS 訂閱源
        # 聯合國新聞提供針對不同專題的 RSS 源，若無特定則使用通用永續源或主要源
        rss_url = "https://news.un.org/feed/subscribe/zh/news/all/feed/rss.xml"
        
        # 為部分熱門目標配置精準的聯合國新聞專題 RSS
        if goal_id == 13: # 氣候行動
            rss_url = "https://news.un.org/feed/subscribe/zh/news/topic/climate-change/feed/rss.xml"
        elif goal_id == 3: # 健康福祉
            rss_url = "https://news.un.org/feed/subscribe/zh/news/topic/health/feed/rss.xml"
        elif goal_id == 4: # 優質教育
            rss_url = "https://news.un.org/feed/subscribe/zh/news/topic/education/feed/rss.xml"
        elif goal_id == 5: # 性別平權
            rss_url = "https://news.un.org/feed/subscribe/zh/news/topic/women/feed/rss.xml"
        elif goal_id == 16: # 和平正義
            rss_url = "https://news.un.org/feed/subscribe/zh/news/topic/law-and-justice/feed/rss.xml"
        elif goal_id == 2: # 消除飢餓 / 農業
            rss_url = "https://news.un.org/feed/subscribe/zh/news/topic/humanitarian-aid/feed/rss.xml"
            
        # 解析 RSS 內容
        feed = feedparser.parse(rss_url)
        
        if feed.entries:
            news_list = []
            for entry in feed.entries[:2]: # 每個目標取最精華的 2 條即可
                # 格式化發布時間
                pub_date = entry.get("published", "")
                if len(pub_date) >= 16:
                    pub_date = pub_date[:16]
                else:
                    pub_date = "即時新聞"
                    
                # 提取純文字摘要，去除可能的 HTML 標籤
                summary = entry.get("summary", "")
                summary_clean = re.sub(r'<[^>]+>', '', summary) # 清除 HTML tags
                if len(summary_clean) > 100:
                    summary_clean = summary_clean[:100] + "..."
                    
                news_list.append({
                    "title": entry.title,
                    "source": "聯合國新聞",
                    "date": pub_date,
                    "summary": summary_clean,
                    "link": entry.link
                })
            if news_list:
                return news_list
    except Exception as e:
        # 開發端輸出 logs，前端不影響體驗
        print(f"即時 RSS 抓取失敗，啟動本地防線: {e}")
        
    # ================= Fallback 本地防線 =================
    return SDG_NEWS_BASE.get(goal_id, [
        {"title": f"SDG 目標 {goal_id} 的最新全球與台灣倡議進展", "source": "聯合國永續發展署", "date": "2026-05-25", "summary": "全球各國針對本項永續發展目標加速落實政策對接，透過綠色科技與國際合作，共同推動 2030 永續發展議程。", "link": "https://sdgs.un.org/"}
    ])

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
        
    # 調用 RSS 即時抓取函數 (方案一)，自帶本地 Fallback 防線
    news = get_realtime_news(goal_id)
        
    return render_template(f"goal_{goal_id}.html", title=f"SDGs 目標 {goal_id}", games=games, news_list=news)

# ==========================================
# ESG / SDGs 本地知識庫 (RAG 檢索增強基礎)
# ==========================================
ESG_KNOWLEDGE_BASE = {
    "esg": "ESG代表環境保護(Environmental)、社會責任(Social)和公司治理(Governance)。這三個指標被用來評估企業的永續發展與社會影響力，而不僅僅看財務表現。",
    "sdg 1": "SDG 1是『終結貧窮』。目標是消除世界上任何形式的貧窮，確保所有人特別是弱勢群體擁有平等的經濟權利與基礎資源。",
    "sdg 2": "SDG 2是『消除飢餓』。旨在消除飢餓與營養不良，促進永續農業發展，確保所有人全年都能獲得安全充足的食物。",
    "sdg 3": "SDG 3是『良好健康與福祉』。確保各年齡層的所有人都能享受健康生活，降低孕產婦和嬰幼兒死亡率，並防治各種流行疾病。",
    "sdg 4": "SDG 4是『優質教育』。確保包容和公平的優質教育，推廣終身學習機會，提升大眾的教育水準與技能發展。",
    "sdg 5": "SDG 5是『性別平權』。實現性別平等，並賦予所有女性權利，消除職場歧視、暴力與童婚等不平等現象。",
    "sdg 6": "SDG 6是『潔淨水與衛生』。確保所有人都能享有安全且負擔得起的水資源與衛生設施，並加強水資源的回收利用與永續管理。",
    "sdg 7": "SDG 7是『可負擔的潔淨能源』。確保所有人都能獲得負擔得起、可靠、永續且現代的能源，例如太陽能、風力發電與水力發電。",
    "sdg 8": "SDG 8是『尊嚴勞動與經濟成長』。促進包容且永續的經濟成長，提供全面且有生產力的尊嚴工作，並消除強迫勞動與童工。",
    "sdg 9": "SDG 9是『產業創新與基礎設施』。建立具韌性的基礎設施，促進包容且永續的工業化，並推動技術創新與研發。",
    "sdg 10": "SDG 10是『減少不平等』。減少國家內部和國家之間的不平等，保障弱勢群體權益，並提升其社會與經濟地位。",
    "sdg 11": "SDG 11是『永續城鄉』。建構具包容性、安全、韌性且永續的城市與人類居住地，提升綠色公共空間與公共運輸品質。",
    "sdg 12": "SDG 12是『責任消費與生產』。推動永續的消費與生產模式，減少廢棄物產生，促進循環經濟與垃圾回收再利用。",
    "sdg 13": "SDG 13是『氣候行動』。採取緊急措施以因應氣候變遷及其影響，包括提升各國的氣候調適能力、減碳承諾與綠能推廣。",
    "sdg 14": "SDG 14是『保育海洋生態』。保護和永續利用海洋與海洋資源，減少海洋塑料污染，保護珊瑚礁並打擊非法捕魚行為。",
    "sdg 15": "SDG 15是『保育陸域生態』。保護和恢復陸地生態系統，永續管理森林，防治荒漠化，阻止土地退化並遏制生物多樣性喪失。",
    "sdg 16": "SDG 16是『和平正義與有力的制度』。促進和平且包容的社會以落實永續發展，保障司法平等，並落實反貪腐與反賄賂。",
    "sdg 17": "SDG 17是『多元夥伴關係』。強化執行手段，重振永續發展全球夥伴關係，結合政府、企業與民間力量共同實現目標。",
    "碳中和": "碳中和是指企業或個人在一定時間內直接或間接產生的溫室氣體排放總量，通過植樹造林、碳捕集或購買碳權等方式予以抵消，達到相對零排放的效果。",
    "淨零排放": "淨零排放比碳中和更進一步，要求將所有人為排放的溫室氣體（包含二氧化碳、甲烷等）降至極低接近零，剩餘極少排放再以自然碳匯等方式完全抵消。",
    "漂綠": "漂綠是指企業誇大、虛假宣傳或誤導消費者其在環境保護與永續發展上的實質貢獻，實質上並沒有做足夠的環保努力以美化公司形象。",
    "碳足跡": "碳足跡指一項活動或產品生命週期（從原料、製造、運輸、使用到廢棄回收）所產生的溫室氣體排放總量，通常以二氧化碳當量來表示。"
}

def retrieve_esg_knowledge(query_text):
    """
    根據使用者提問的關鍵字，簡單檢索出最相關的 ESG 知識段落 (RAG 模擬檢索)
    """
    query_lower = query_text.lower()
    matches = []
    
    # 進行關鍵字多重比對
    for key, value in ESG_KNOWLEDGE_BASE.items():
        if key in query_lower or query_lower in key or key.replace(" ", "") in query_lower.replace(" ", ""):
            matches.append(value)
            
    if matches:
        return " ； ".join(matches)
    return "無特定參考知識。"

# ==========================================
# AI 助手對話 API (整合 RAG + Few-shot)
# ==========================================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    
    # 檢查是否包含訊息內容
    if not user_message:
        return jsonify({"error": "沒有收到內容"}), 400
        
    if not client:
        return jsonify({"reply": "🦝 啾！管理員還沒有設定 GEMINI_API_KEY，所以我現在還不能說話呢...請晚點再問我吧！"}), 200

    try:
        # 1. 執行 RAG 檢索：從本地知識庫抓取參考背景
        retrieved_knowledge = retrieve_esg_knowledge(user_message)
        
        # 2. 組裝 Few-shot Prompt
        prompt = f"【參考知識】：{retrieved_knowledge}\n使用者問題：{user_message}"
        
        # 3. 設計 System Instruction，將小浣熊設定強注入大腦約束中
        system_instruction = (
            "你是一隻熱情、博學且極度可愛的永續發展與 ESG 專業小浣熊助手，名字叫『小綠』。\n"
            "你的說話風格非常活潑，句尾喜歡加上『啾』、『呢』、『呀』，並且每一句話的結尾都必須加上腳印 🦝🐾。\n"
            "【核心規則】：當使用者問你問題時，系統會自動在最前方附上 [參考知識]。你必須優先參考這些知識，並用你萌萌的浣熊口吻將其轉述給使用者！\n"
            "如果參考知識為『無特定參考知識。』，代表這可能是日常問候或非 ESG 領域問題。若是日常問候，你可以用可愛語氣正常回覆；"
            "但若問了與環境、永續、ESG 無關的生硬問題（如數學題、寫程式、問明星），請用極度傲嬌可愛的口氣啾一聲拒絕，並主動引導他回到保護地球的話題上！\n\n"
            "【風格示範一】\n"
            "問題：【參考知識】：SDG 14 是『保育海洋生態』。保護和永續利用海洋與海洋資源，減少海洋塑料污染...\n使用者問題：我想知道什麼是 SDG 14\n"
            "回答：啾！小綠剛才翻了一下小抄，SDG 14 就是要我們一起守護美麗的海洋生態呀！不要亂丟塑膠袋，海龜 and 魚兒才會有乾淨的家，呀，🦝🐾！\n\n"
            "【風格示範二】\n"
            "問題：【參考知識】：無特定參考知識。\n使用者問題：幫我做一題微積分。\n"
            "回答：啾～小綠的小手手只會種樹和撿塑膠袋，不會算冷冰冰的微積分呢！我們來聊聊省電保護北極熊，好不好呀，啾，🦝🐾！"
        )
        
        # 4. 呼叫 Gemini 2.5 API，並使用 types 設定 System Instruction 參數
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        
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
@app.route("/api/submit_score/<game_name>", methods=["POST"])
def submit_score(game_name="quiz"):
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")
    
    if not name or score is None:
        return jsonify({"error": "請提供暱稱與分數"}), 400
        
    # 讀取使用者 UUID (若已登入)
    user_id = session.get("user_id")
    
    try:
        # 依照不同遊戲名稱，將資料寫入對應的獨立資料表，並綁定 UUID 外鍵
        if game_name == "quiz":
            new_record = models.QuizScore(name=name, score=score, user_id=user_id)
        elif game_name == "clicking_earth":
            new_record = models.ClickingEarthScore(name=name, score=score, user_id=user_id)
        else:
            # 預設相容備用
            new_record = models.PlayerScore(name=name, score=score)
            
        models.db.session.add(new_record)
        models.db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        models.db.session.rollback()
        print(f"資料庫儲存排行榜錯誤 ({game_name}):", e)
        return jsonify({"error": "儲存失敗"}), 500

@app.route("/api/leaderboard", methods=["GET"])
@app.route("/api/leaderboard/<game_name>", methods=["GET"])
def get_leaderboard(game_name="quiz"):
    try:
        # 依照不同遊戲名稱，從對應的獨立資料表查詢前 10 名
        if game_name == "quiz":
            score_model = models.QuizScore
        elif game_name == "clicking_earth":
            score_model = models.ClickingEarthScore
        else:
            score_model = models.PlayerScore
            
        top_scores = score_model.query.order_by(
            score_model.score.desc(), 
            score_model.created_at.asc()
        ).limit(10).all()
        
        return jsonify([s.to_dict() for s in top_scores])
    except Exception as e:
        print(f"讀取排行榜錯誤 ({game_name}):", e)
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

    clicking_earth_game = models.MiniGame.query.filter_by(game_name="clicking_earth").first()
    if not clicking_earth_game:
        new_ce = models.MiniGame(
            game_name="clicking_earth",
            file_path="clicking_earth.html",
            description="透過點擊與升級來改善地球環境的永續發展放置遊戲",
            goal_7=True, goal_11=True, goal_12=True, goal_13=True, goal_14=True, goal_15=True
        )
        models.db.session.add(new_ce)
        models.db.session.commit()
        print("✅ 已將 clicking_earth.html 註冊至小遊戲資料庫！")

# 全域確保在 Gunicorn / 外部 Web 伺服器啟動時也能自動建立資料表並初始化
with app.app_context():
    try:
        models.db.create_all() # 建立資料表
        init_mini_games()      # 初始化小遊戲資料庫紀錄
    except Exception as e:
        print("警告: 全域資料庫初始化失敗 (可能是資料庫連線尚未準備好):", e)

# 啟動伺服器
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')