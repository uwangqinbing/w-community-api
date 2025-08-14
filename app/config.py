import os

class Config:
    # 通用配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'w-community-web-jwt-secret')  # 建议生产环境用环境变量
    JWT_SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = 'public'
    CORS_ORIGINS = "http://localhost:5173"

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:180081@localhost:3306/w_community?charset=utf8mb4"

class ProductionConfig(Config):
    # 生产环境配置（建议用环境变量）
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

# 默认使用开发环境配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}