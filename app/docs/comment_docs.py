from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.models.comment import Comment
from app.extensions import db
from datetime import datetime
from app.models.post import Post

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
@comment_ns.route('/posts/<int:post_id>/comments', endpoint='create_comment')  # 显式指定端点
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
    
@comment_ns.route('/comments/<int:comment_id>', endpoint='delete_comment')  # 显式指定端点
class CommentDeleteDoc(Resource):
    @jwt_required()
    def delete(self, comment_id):
        """删除评论（需登录，根据权限控制）"""
        """
        权限说明：
        - 超级管理员：可以删除所有评论
        - 版主：可以删除自己板块下的评论
        - 普通用户：只能删除自己的评论
        """
        current_email = get_jwt_identity()
        user = UserService.get_user_by_email(current_email)
        if not user:
            return {'msg': '用户不存在'}, 404
        
        comment = Comment.query.get(comment_id)
        if not comment:
            return {'msg': '评论不存在'}, 404
            
        post = Post.query.get(comment.post_id)
        if not post:
            return {'msg': '评论所属帖子不存在'}, 404
            
        # 权限检查逻辑（与路由中相同）
        if not (user.is_admin() or 
                (user.is_moderator() and post.section in (user.moderator_for.split(',') if user.moderator_for else [])) or
                comment.author == user.username):
            return {'msg': '没有权限删除此评论'}, 403
            
        db.session.delete(comment)
        db.session.commit()
        return {'msg': '评论已成功删除'}, 200