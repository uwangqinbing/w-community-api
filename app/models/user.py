from app.extensions import db

class User(db.Model):
    __tablename__ = 'user'  # 显式指定表名

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # 生产环境需加密
    avatar = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "avatar": self.avatar
        }