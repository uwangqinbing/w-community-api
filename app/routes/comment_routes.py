from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.extensions import db
from app.models.comment import Comment
from app.models.user import User
from app.models.post import Post
from app.services.user_service import UserService

# 确保蓝图名称与其他蓝图不冲突
comment_bp = Blueprint('comment_bp', __name__, url_prefix='/api')

@comment_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    """添加评论接口"""
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({"error": "评论内容不能为空"}), 400

    current_email = get_jwt_identity()
    user = User.query.filter_by(email=current_email).first()
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    new_comment = Comment(
        post_id=post_id,
        author=user.username,
        authorAvatar=user.avatar or '/OIP-C.webp',
        content=data['content'],
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    try:
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment_by_id(comment_id):  # 修改函数名，避免与蓝图名组合后重复
    """删除评论接口（带权限控制）"""
    # 1. 获取当前登录用户信息
    current_email = get_jwt_identity()
    current_user = UserService.get_user_by_email(current_email)
    if not current_user:
        return jsonify({"error": "用户不存在"}), 404
    
    # 2. 获取要删除的评论
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "评论不存在"}), 404
    
    # 3. 获取评论所属的帖子
    post = Post.query.get(comment.post_id)
    if not post:
        return jsonify({"error": "评论所属帖子不存在"}), 404
    
    # 4. 权限检查
    # 4.1 超级管理员可以删除所有评论
    if current_user.is_admin():
        pass  # 有权限，继续执行删除
    # 4.2 版主可以删除自己板块下的评论
    elif current_user.is_moderator():
        # 检查帖子板块是否在版主管理范围内
        moderator_sections = current_user.moderator_for.split(',') if current_user.moderator_for else []
        if post.section not in moderator_sections:
            return jsonify({"error": "没有权限删除此评论"}), 403
    # 4.3 普通用户只能删除自己的评论
    else:
        # 检查评论作者是否为当前用户
        if comment.author != current_user.username:
            return jsonify({"error": "没有权限删除此评论"}), 403
    
    # 5. 执行删除操作
    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "评论已成功删除"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
