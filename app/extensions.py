from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

# 初始化扩展（暂不绑定app）
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
migrate = Migrate()