from flask import Blueprint, request, jsonify
from app.services.user_service import UserService  # 业务逻辑导入

user_bp = Blueprint('user', __name__, url_prefix='/api')  # ✅ 这行是蓝图的定义

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    result, status = UserService.register(
        email=data.get('email'),
        password=data.get('password')
    )
    return jsonify(result), status