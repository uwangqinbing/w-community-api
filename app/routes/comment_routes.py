from flask import Blueprint

comment_bp = Blueprint('comment', __name__, url_prefix='/api')

@comment_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    return {"msg": "评论接口待实现"}, 200