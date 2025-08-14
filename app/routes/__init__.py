from .user_routes import user_bp    # 注意用相对路径：.user_routes（当前包内的user_routes.py）
from .post_routes import post_bp
from .comment_routes import comment_bp  # 确保comment_routes.py中定义了comment_bp

# 可选：显式声明可导出的蓝图（避免导入时找不到）
__all__ = ['user_bp', 'post_bp', 'comment_bp']