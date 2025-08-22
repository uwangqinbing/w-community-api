from flask import Flask
from flask_cors import CORS  # 只需要导入一次
from app.config import config
from app.extensions import db, jwt, migrate  # 移除重复的 cors 导入
from app.routes import user_bp, post_bp, comment_bp
from app.docs import docs_bp
from app.routes.report_routes import report_bp

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='../public')
    app.config.from_object(config[config_name])

    # 初始化扩展（顺序无关）
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # 关键：只配置一次 CORS，合并所有规则
    CORS(app, 
         resources={
             r"/api/*": {  # 对所有 /api 前缀接口生效
                 "origins": "http://localhost:5173",  # 允许前端地址
                 "supports_credentials": True,  # 允许携带 Token/Cookie
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]  # 包含所有需要的方法
             }
         },
         # 全局默认配置（可选，这里留空避免冲突）
         origins=app.config.get('CORS_ORIGINS', []),
         supports_credentials=True
    )

    # 注册蓝图（确保所有蓝图路径正确）
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)  # 确保 post_bp 注册时带了 /api 前缀
    app.register_blueprint(comment_bp)
    app.register_blueprint(report_bp) # 举报功能的蓝图必须注册
    app.register_blueprint(docs_bp)

    # 静态资源路由
    @app.route('/public/<path:filename>')
    def serve_public(filename):
        return app.send_static_file(filename)

    return app