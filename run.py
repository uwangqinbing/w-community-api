from app import create_app
from app.extensions import db
from app.models.user import User  
from app.models.post import Post  
from app.models.comment import Comment

app = create_app()

_data_initialized = False

@app.before_request
def init_test_data():
    global _data_initialized
    if not _data_initialized:
        with app.app_context():
            if not User.query.first():
                from datetime import datetime
                # 创建测试用户
                user1 = User(username="TechLover", email="tech@example.com", password="123456", avatar="/OIP-C.webp")
                user2 = User(username="GamerPro", email="game@example.com", password="123456", avatar="/OIP-C.webp")
                db.session.add_all([user1, user2])
                db.session.commit()
                
                # 创建测试帖子
                post1 = Post(
                    title="测试帖子1",
                    content="这是第一个测试帖子",
                    authorId=user1.id,
                    date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    tags="测试,技术",
                    type="posts",
                    image="",
                    likes=0
                )
                post2 = Post(
                    title="测试帖子2",
                    content="这是第二个测试帖子",
                    authorId=user2.id,
                    date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    tags="测试,生活",
                    type="posts",
                    image="",
                    likes=0
                )
                db.session.add_all([post1, post2])
                db.session.commit()
        _data_initialized = True

if __name__ == '__main__':
    app.run(debug=True, port=5000)