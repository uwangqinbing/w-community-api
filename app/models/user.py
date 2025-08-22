from app.extensions import db

class User(db.Model):
    __tablename__ = 'user'  # 显式指定表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # 生产环境需加密
    avatar = db.Column(db.String(200))
    role = db.Column(db.String(20), default='user', nullable=False)
    moderator_for = db.Column(db.String(100)) 

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "avatar": self.avatar,
            "role": self.role,
            "moderator_for": self.moderator_for
        }
    
    # 辅助方法，检查是否为超级管理员
    def is_admin(self):
        return self.role == 'admin'
    
    # 辅助方法，检查是否为版主
    def is_moderator(self):
        return self.role == 'moderator'