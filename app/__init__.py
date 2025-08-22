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

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    CORS(app, 
         resources={
             r"/api/*": {
                 "origins": "http://localhost:5173",
                 "supports_credentials": True,
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
             }
         },
    )

    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(docs_bp)

    # 静态资源路由
    @app.route('/public/<path:filename>')
    def serve_public(filename):
        return app.send_static_file(filename)

    return app