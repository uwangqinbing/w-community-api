from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.models.comment import Comment
from app.extensions import db
from datetime import datetime

# 定义命名空间
comment_ns = Namespace('评论管理', description='帖子评论接口')

# 评论请求模型
comment_create_model = comment_ns.model('创建评论', {
    'content': fields.String(required=True, description='评论内容')
})

# 评论响应模型
comment_model = comment_ns.model('评论信息', {
    'id': fields.Integer(description='评论ID'),
    'author': fields.String(description='评论作者'),
    'authorAvatar': fields.String(description='作者头像'),
    'content': fields.String(description='评论内容'),
    'date': fields.String(description='评论时间')
})

# 评论接口
@comment_ns.route('/posts/<int:post_id>/comments')
class CommentDoc(Resource):
    @jwt_required()
    @comment_ns.expect(comment_create_model)
    @comment_ns.marshal_with(comment_model)
    def post(self, post_id):
        """添加帖子评论（需登录）"""
        current_email = get_jwt_identity()
        user = UserService.get_user_by_email(current_email)
        if not user:
            return {'msg': '用户不存在'}, 404
        
        data = comment_ns.payload
        if not data.get('content'):
            return {'msg': '评论内容不能为空'}, 400
        
        new_comment = Comment(
            post_id=post_id,
            author=user.username,
            authorAvatar=user.avatar,
            content=data.get('content'),
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment.to_dict()