from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

# 宣告未綁定的資料庫物件
db = SQLAlchemy()

# 設定 Argon2id 參數（符合 OWASP 建議）
# time_cost=3 表示迭代3次；memory_cost=65536 = 64MB；parallelism=2 表示2條執行緒
_ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16,
    encoding="utf-8"
)

# ==========================================
# 使用者帳號資料表（僅存非敏感資訊）
# ==========================================
class User(db.Model):
    __tablename__ = "user"

    # UUID 主鍵：對外暴露時不可猜測
    id         = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username   = db.Column(db.String(50),  unique=True, nullable=False)   # 顯示名稱（排行榜用）
    email      = db.Column(db.String(120), unique=True, nullable=False)   # 登入用電子信箱
    created_at = db.Column(db.DateTime, default=datetime.utcnow)          # 帳號建立時間
    last_login = db.Column(db.DateTime, nullable=True)                    # 最後登入時間
    deleted_at = db.Column(db.DateTime, nullable=True)                    # 軟刪除欄位 (None表示未刪除)

    # 關聯到密碼憑證表（一對一）
    credential = db.relationship("UserCredential", back_populates="user",
                                 uselist=False, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        """顯式建構子，用於消除 IDE / Pylance 的型別檢查警告並提供自動補全"""
        super().__init__(**kwargs)

    def soft_delete(self):
        """軟刪除使用者，記錄刪除時間"""
        self.deleted_at = datetime.utcnow()

    @property
    def is_deleted(self) -> bool:
        """判斷是否已被軟刪除"""
        return self.deleted_at is not None

    def to_dict(self):
        return {
            "id":         self.id,
            "username":   self.username,
            "email":      self.email,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }

# ==========================================
# 使用者密碼憑證資料表（與帳號資料分離）
# ==========================================
class UserCredential(db.Model):
    __tablename__ = "user_credential"

    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), unique=True, nullable=False)

    # Salt：每位使用者獨立產生的 16 bytes 隨機值（hex 字串儲存）
    salt          = db.Column(db.String(64),  nullable=False)

    # Argon2id hash 結果（PHC 格式，已包含演算法參數）
    password_hash = db.Column(db.String(512), nullable=False)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 反向關聯
    user = db.relationship("User", back_populates="credential")

    def __init__(self, **kwargs):
        """顯式建構子，用於消除 IDE / Pylance 的型別檢查警告並提供自動補全"""
        super().__init__(**kwargs)

    @staticmethod
    def hash_password(plain_password: str) -> tuple[str, str]:
        """
        產生 salt 並用 Argon2id 雜湊密碼。
        回傳 (salt_hex, argon2id_hash_string)
        """
        # 產生 16 bytes 的隨機 salt
        salt_bytes = os.urandom(16)
        salt_hex   = salt_bytes.hex()  # 轉成 hex 字串存入資料庫

        # 將 salt 附加至密碼再做 Argon2id 雜湊
        # 這樣即使兩人密碼相同，hash 也會不同
        salted_password = salt_hex + plain_password
        hash_str        = _ph.hash(salted_password)

        return salt_hex, hash_str

    def verify_password(self, plain_password: str) -> bool:
        """
        驗證明文密碼是否與資料庫中的 hash 相符。
        回傳 True（相符）或 False（不符）。
        """
        try:
            salted_password = self.salt + plain_password
            return _ph.verify(self.password_hash, salted_password)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False

    def needs_rehash(self) -> bool:
        """若 Argon2 參數已更新，回傳 True 提示應重新雜湊。"""
        return _ph.check_needs_rehash(self.password_hash)

class Event(db.Model):
    id = db.Column(db.String(36), primary_key=True)

    def __init__(self, **kwargs):
        """顯式建構子，用於消除 IDE / Pylance 的型別檢查警告並提供自動補全"""
        super().__init__(**kwargs)

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

    def __init__(self, **kwargs):
        """顯式建構子，用於消除 IDE / Pylance 的型別檢查警告並提供自動補全"""
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

# ==========================================
# 知識大挑戰（Quiz）獨立排行榜資料表
# ==========================================
class QuizScore(db.Model):
    __tablename__ = "quiz_score"

    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), unique=False, nullable=True) # UUID 外來鍵
    name    = db.Column(db.String(50), nullable=False)
    score   = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)                    # 軟刪除欄位 (None表示未刪除)

    # 關聯至 User
    user = db.relationship("User")

    def __init__(self, **kwargs):
        """顯式建構子，用於消除 IDE / Pylance 的型別檢查警告並提供自動補全"""
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "user_id": self.user_id
        }

# ==========================================
# Clicking Earth 獨立排行榜資料表
# ==========================================
class ClickingEarthScore(db.Model):
    __tablename__ = "clicking_earth_score"

    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), unique=False, nullable=True) # UUID 外來鍵
    name    = db.Column(db.String(50), nullable=False)
    score   = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)                    # 軟刪除欄位 (None表示未刪除)

    # 關聯至 User
    user = db.relationship("User")

    def __init__(self, **kwargs):
        """顯式建構子，用於消除 IDE / Pylance 的型別檢查警告並提供自動補全"""
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "user_id": self.user_id
        }

# 小遊戲與 ESG 目標關聯模型
class MiniGame(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_name = db.Column(db.String(100), nullable=False) # 遊戲名稱 (例如：quiz)
    file_path = db.Column(db.String(255), nullable=True)  # 網頁檔案路徑 (例如：quiz.html)
    description = db.Column(db.Text, nullable=True)       # 遊戲簡介
    deleted_at = db.Column(db.DateTime, nullable=True)                    # 軟刪除欄位 (None表示未刪除)
    
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

    def __init__(self, **kwargs):
        """顯式建構子，用於消除 IDE / Pylance 的型別檢查警告並提供自動補全"""
        super().__init__(**kwargs)

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