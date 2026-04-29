from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 宣告未綁定的資料庫物件
db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.String(36), primary_key=True)

    def to_dict(self):
        return {
            "id": self.id,
        }

# 排行榜分數模型
class PlayerScore(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

# 小遊戲與 ESG 目標關聯模型
class MiniGame(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_name = db.Column(db.String(100), nullable=False) # 遊戲名稱 (例如：quiz)
    file_path = db.Column(db.String(255), nullable=True)  # 網頁檔案路徑 (例如：quiz.html)
    description = db.Column(db.Text, nullable=True)       # 遊戲簡介
    
    # 17 個屬性對應 17 個 SDGs 目標 (True 代表該遊戲有涵蓋該目標)
    goal_1 = db.Column(db.Boolean, default=False)
    goal_2 = db.Column(db.Boolean, default=False)
    goal_3 = db.Column(db.Boolean, default=False)
    goal_4 = db.Column(db.Boolean, default=False)
    goal_5 = db.Column(db.Boolean, default=False)
    goal_6 = db.Column(db.Boolean, default=False)
    goal_7 = db.Column(db.Boolean, default=False)
    goal_8 = db.Column(db.Boolean, default=False)
    goal_9 = db.Column(db.Boolean, default=False)
    goal_10 = db.Column(db.Boolean, default=False)
    goal_11 = db.Column(db.Boolean, default=False)
    goal_12 = db.Column(db.Boolean, default=False)
    goal_13 = db.Column(db.Boolean, default=False)
    goal_14 = db.Column(db.Boolean, default=False)
    goal_15 = db.Column(db.Boolean, default=False)
    goal_16 = db.Column(db.Boolean, default=False)
    goal_17 = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "game_name": self.game_name,
            "file_path": self.file_path,
            "description": self.description,
            "goals": {
                "1": self.goal_1, "2": self.goal_2, "3": self.goal_3, "4": self.goal_4,
                "5": self.goal_5, "6": self.goal_6, "7": self.goal_7, "8": self.goal_8,
                "9": self.goal_9, "10": self.goal_10, "11": self.goal_11, "12": self.goal_12,
                "13": self.goal_13, "14": self.goal_14, "15": self.goal_15, "16": self.goal_16,
                "17": self.goal_17
            }
        }