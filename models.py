# models.py
from flask_sqlalchemy import SQLAlchemy
# 宣告一個還沒有跟 app 綁定的資料庫物件
db = SQLAlchemy()
# 將 main.py 裡面的 Event 類別剪下並貼到這裡
class Event(db.Model):
    id = db.Column(db.String(36), primary_key=True)

    def to_dict(self):
        return {
            "id": self.id,

        }