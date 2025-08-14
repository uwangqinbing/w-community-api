from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token

class UserService:
    @staticmethod
    def register(email, password, username=None, avatar=None):
        # 检查邮箱是否已注册
        if User.query.filter_by(email=email).first():
            return {"msg": "邮箱已注册"}, 400
        
        # 生成默认用户名（邮箱@前的内容）
        username = username or email.split('@')[0]
        # 默认头像
        avatar = avatar or '/OIP-C.webp'
        
        # 创建用户
        new_user = User(
            email=email,
            password=password,  # 生产环境需加密（如bcrypt.hashpw）
            username=username,
            avatar=avatar
        )
        db.session.add(new_user)
        db.session.commit()
        
        # 生成JWT令牌
        token = create_access_token(identity=email)
        return {
            "token": token,
            "user": new_user.to_dict()
        }, 201

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if not user or user.password != password:  # 生产环境需解密验证
            return {"msg": "登录失败"}, 401
        
        token = create_access_token(identity=email)
        return {
            "token": token,
            "user": user.to_dict()
        }, 200

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()