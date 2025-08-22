from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.extensions import db
from app.models.comment import Comment
from app.models.user import User

comment_bp = Blueprint('comment', __name__, url_prefix='/api')

@comment_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
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