from app import create_app
from app.extensions import db
from app.models.user import User  
from app.models.post import Post  
from app.models.comment import Comment
from datetime import datetime

app = create_app()

@app.route('/')  
def hello():
    # 查询当前用户总数（示例，可根据需求扩展）
    user_count = User.query.count()
    post_count = Post.query.count()
    return f"欢迎访问社区论坛 API 根路径！当前有 {user_count} 位用户，{post_count} 篇帖子～"

_data_initialized = False

@app.before_request
def init_test_data():
    global _data_initialized
    if not _data_initialized:
        with app.app_context():
            if not User.query.first():
                # 创建测试用户
                user1 = User(
                    username="TechLover", 
                    email="tech@example.com", 
                    password="123456", 
                    avatar="/OIP-C.webp",
                    role="user"  # 添加角色字段
                )
                user2 = User(
                    username="GamerPro", 
                    email="game@example.com", 
                    password="123456", 
                    avatar="/OIP-C.webp",
                    role="user"  # 添加角色字段
                )
                
                # 创建管理员用户
                admin = User(
                    username="Admin", 
                    email="admin@example.com", 
                    password="admin123",  # 生产环境需修改
                    avatar="/OIP-C.webp",
                    role="admin"
                )
                
                # 创建版主用户
                moderator = User(
                    username="Moderator", 
                    email="moderator@example.com", 
                    password="mod123",  # 生产环境需修改
                    avatar="/OIP-C.webp",
                    role="moderator",
                    moderator_for="tech,games"  # 管理tech和games板块
                )
                
                # 批量添加用户
                db.session.add_all([user1, user2, admin, moderator])
                db.session.commit()  # 先提交用户，获取用户ID
                
                # 创建测试帖子（依赖用户ID）
                post1 = Post(
                    title="测试帖子1",
                    content="这是第一个测试帖子",
                    authorId=user1.id,
                    date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    tags="测试,技术",
                    type="posts",
                    image="",
                    likes=0,
                    section="tech"  # 添加板块字段
                )
                post2 = Post(
                    title="测试帖子2",
                    content="这是第二个测试帖子",
                    authorId=user2.id,
                    date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    tags="测试,生活",
                    type="posts",
                    image="",
                    likes=0,
                    section="games"  # 添加板块字段
                )
                db.session.add_all([post1, post2])
                db.session.commit()
        
        _data_initialized = True

if __name__ == '__main__':
    app.run(debug=True, port=5000)