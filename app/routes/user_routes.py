from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/api')

@user_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册接口
    ---
    接收邮箱、密码，创建新用户并返回用户信息
    """
    data = request.json
    result, status = UserService.register(
        email=data.get('email'),
        password=data.get('password')
    )
    return jsonify(result), status

# 登录接口
@user_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录接口
    ---
    接收邮箱、密码，校验成功后返回 JWT Token 和用户信息
    """
    data = request.json
    result, status = UserService.login(
        email=data.get('email'),
        password=data.get('password')
    )
    return jsonify(result), status