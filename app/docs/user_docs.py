from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

# 定义命名空间
user_ns = Namespace('用户管理', description='用户注册和登录接口')

# 注册请求参数模型
register_model = user_ns.model('用户注册', {
    'email': fields.String(required=True, description='用户邮箱（登录账号）'),
    'password': fields.String(required=True, description='用户密码'),
    'username': fields.String(required=False, description='用户名（可选，默认取邮箱@前内容）'),
    'avatar': fields.String(required=False, description='头像URL（可选，默认使用系统头像）')
})

# 登录请求参数模型
login_model = user_ns.model('用户登录', {
    'email': fields.String(required=True, description='用户邮箱'),
    'password': fields.String(required=True, description='用户密码')
})

# 1. 先定义独立的用户信息模型（关键修复）
user_info_model = user_ns.model('用户信息', {
    'id': fields.Integer(description='用户ID'),
    'email': fields.String(description='用户邮箱'),
    'username': fields.String(description='用户名'),
    'avatar': fields.String(description='头像URL')
})

# 2. 在响应模型中引用用户信息模型
user_response = user_ns.model('用户响应', {
    'token': fields.String(description='JWT令牌（用于认证）'),
    'user': fields.Nested(user_info_model)  # 引用上面定义的user_info_model
})

# 注册接口文档
@user_ns.route('/register')
class RegisterDoc(Resource):
    @user_ns.expect(register_model)
    @user_ns.marshal_with(user_response)
    def post(self):
        """用户注册"""
        data = user_ns.payload
        result, status = UserService.register(
            email=data.get('email'),
            password=data.get('password'),
            username=data.get('username'),
            avatar=data.get('avatar')
        )
        return result, status

# 登录接口文档
@user_ns.route('/login')
class LoginDoc(Resource):
    @user_ns.expect(login_model)
    @user_ns.marshal_with(user_response)
    def post(self):
        """用户登录（返回JWT令牌）"""
        data = user_ns.payload
        result, status = UserService.login(
            email=data.get('email'),
            password=data.get('password')
        )
        return result, status