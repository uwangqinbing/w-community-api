from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.extensions import db
from app.models.comment import Comment  # 假设Comment模型在models目录下
from app.models.user import User  # 假设存在User模型
from app.services.user_service import UserService

comment_bp = Blueprint('comment', __name__, url_prefix='/api')

@comment_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()  # 需要登录才能评论
def add_comment(post_id):
    # 1. 获取请求数据
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({"error": "评论内容不能为空"}), 400

    # 2. 获取当前登录用户信息
    current_email = get_jwt_identity()
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    # 3. 创建评论对象
    new_comment = Comment(
        post_id=post_id,
        author=user.username,  # 假设User模型有username字段
        authorAvatar=user.avatar or '/OIP-C.webp',  # 假设User模型有avatar字段
        content=data['content'],
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
    )

    # 4. 保存到数据库
    try:
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.to_dict()), 201  # 返回创建的评论
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500