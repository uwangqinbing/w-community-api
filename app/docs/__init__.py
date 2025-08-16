from flask_restx import Api
from flask import Blueprint

# 创建 Swagger 专用蓝图（路径前缀为 /docs，避免与现有接口冲突）
docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

# 初始化 Swagger 文档
api = Api(
    docs_bp,
    version='1.0',
    title='社区论坛 API 文档',
    description='支持用户注册、登录、帖子管理、评论和点赞功能的接口文档',
    doc='/',  # 文档访问路径：http://localhost:5000/docs
    contact='开发者',
    license='MIT'
)

# 导入并注册各模块文档（后续步骤实现）
from .user_docs import user_ns
from .post_docs import post_ns
from .comment_docs import comment_ns

api.add_namespace(user_ns, path='/api')  # 与原有接口路径一致
api.add_namespace(post_ns, path='/api')
api.add_namespace(comment_ns, path='/api')

# 新增：测试路由（直接写在 docs_bp 蓝图下）
@docs_bp.route('/test')
def test():
    return "Swagger ", 200  # 访问 /docs/test 时返回此内容