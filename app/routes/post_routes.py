from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_service import PostService
from app.services.user_service import UserService

post_bp = Blueprint('post', __name__, url_prefix='/api')

@post_bp.route('/posts', methods=['GET'])
def get_posts():
    type_filter = request.args.get('type', 'all')
    posts = PostService.get_posts(type_filter)
    return jsonify(posts if posts is not None else [])

@post_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post_detail(post_id):
    post = PostService.get_post_detail(post_id)
    if not post:
        return jsonify({"msg": "帖子不存在"}), 404
    return jsonify(post)

@post_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_email = get_jwt_identity()
    user = UserService.get_user_by_email(current_email)
    if not user:
        return jsonify({"msg": "用户不存在"}), 404
    data = request.json
    # 关键修复3：校验必填字段，避免服务端报错
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"msg": "标题和内容不能为空"}), 400
    result, status = PostService.create_post(user, data)
    return jsonify(result), status

@post_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()  # 要求登录（和现有接口保持一致的认证逻辑）
def toggle_like(post_id):
    """切换帖子点赞状态（点赞/取消点赞）"""
    try:
        # 获取当前登录用户（复用现有逻辑）
        current_email = get_jwt_identity()
        user = UserService.get_user_by_email(current_email)
        if not user:
            return jsonify({"msg": "用户不存在"}), 404
        
        # 调用服务层处理点赞逻辑（需要在PostService中实现toggle_like方法）
        result, status_code = PostService.toggle_like(user.id, post_id)
        return jsonify(result), status_code
    
    except Exception as e:
        # 错误处理（和现有接口保持一致）
        return jsonify({"msg": f"服务器错误：{str(e)}"}), 500