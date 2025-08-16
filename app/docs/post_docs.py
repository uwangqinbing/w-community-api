from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_service import PostService
from app.services.user_service import UserService

# 定义命名空间
post_ns = Namespace('帖子管理', description='帖子CRUD和点赞接口')

# 创建帖子请求模型
post_create_model = post_ns.model('创建帖子', {
    'title': fields.String(required=True, description='帖子标题'),
    'content': fields.String(required=True, description='帖子内容'),
    'tags': fields.String(required=False, description='标签（逗号分隔，如"技术,生活"）'),
    'type': fields.String(required=True, description='帖子类型（posts/questions/videos）'),
    'image': fields.String(required=False, description='图片URL（可选）')
})

# 1. 先定义独立的作者模型（关键修复）
author_model = post_ns.model('作者信息', {
    'id': fields.Integer(description='作者ID'),
    'username': fields.String(description='作者名'),
    'avatar': fields.String(description='作者头像')
})

# 2. 在帖子模型中引用作者模型（使用fields.Nested）
post_model = post_ns.model('帖子信息', {
    'id': fields.Integer(description='帖子ID'),
    'title': fields.String(description='标题'),
    'content': fields.String(description='内容'),
    'author': fields.Nested(author_model),  # 引用上面定义的author_model
    'date': fields.String(description='发布时间'),
    'tags': fields.List(fields.String, description='标签列表'),
    'likes': fields.Integer(description='点赞数'),
    'type': fields.String(description='帖子类型'),
    'image': fields.String(description='图片URL')
})

# 点赞响应模型
like_response = post_ns.model('点赞结果', {
    'likes': fields.Integer(description='最新点赞数'),
    'isLiked': fields.Boolean(description='当前用户是否已点赞')
})

# 帖子列表/创建接口
@post_ns.route('/posts')
class PostListDoc(Resource):
    @post_ns.param('type', '帖子类型筛选（posts/questions/videos，默认返回全部）', required=False)
    @post_ns.marshal_list_with(post_model)
    def get(self):
        """获取帖子列表（支持按类型筛选）"""
        type_filter = self.api.payload.get('type') if self.api.payload else 'all'
        return PostService.get_posts(type_filter)

    @jwt_required()
    @post_ns.expect(post_create_model)
    @post_ns.marshal_with(post_model)
    def post(self):
        """创建帖子（需登录，需携带Authorization头）"""
        current_email = get_jwt_identity()
        user = UserService.get_user_by_email(current_email)
        if not user:
            return {'msg': '用户不存在'}, 404
        data = post_ns.payload
        result, status = PostService.create_post(user, data)
        return result, status

# 帖子详情接口
@post_ns.route('/posts/<int:post_id>')
class PostDetailDoc(Resource):
    @post_ns.marshal_with(post_model)
    def get(self, post_id):
        """获取帖子详情（含评论列表）"""
        return PostService.get_post_detail(post_id)

# 帖子点赞接口
@post_ns.route('/posts/<int:post_id>/like')
class PostLikeDoc(Resource):
    @jwt_required()
    @post_ns.marshal_with(like_response)
    def post(self, post_id):
        """帖子点赞/取消点赞（需登录）"""
        current_email = get_jwt_identity()
        user = UserService.get_user_by_email(current_email)
        if not user:
            return {'msg': '用户不存在'}, 404
        return PostService.toggle_like(user, post_id)
