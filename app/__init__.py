from flask import Flask
from app.config import config
from app.extensions import db, jwt, cors, migrate
from app.routes import user_bp, post_bp, comment_bp

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='../public')
    app.config.from_object(config[config_name])

    # 初始化扩展（新增 migrate 初始化）
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    migrate.init_app(app, db)

    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp)

    # 静态资源路由
    @app.route('/public/<path:filename>')
    def serve_public(filename):
        return app.send_static_file(filename)

    return app