from flask import Flask, jsonify, request,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask(__name__)
# 配置CORS（允许前端访问）
CORS(app, origins="http://localhost:5173", supports_credentials=True)

# 数据库配置（SQLite文件）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STATIC_FOLDER'] = 'public'
db = SQLAlchemy(app)

@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

# JWT配置（密钥用于加密token）
app.config['JWT_SECRET_KEY'] = 'w-community-web-jwt-secret'
jwt = JWTManager(app)

# 关联表：帖子点赞（多对多关系）
post_likes = db.Table(
    'post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


# 用户模型（必须先定义！因为Post依赖User）
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名
    email = db.Column(db.String(120), unique=True, nullable=False)  # 邮箱（登录用）
    password = db.Column(db.String(120), nullable=False)  # 密码（实际项目需加密）
    avatar = db.Column(db.String(200))  # 头像URL

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "avatar": self.avatar
        }


# 评论模型
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # 关联帖子
    author = db.Column(db.String(50), nullable=False)  # 评论作者名
    authorAvatar = db.Column(db.String(100), nullable=False)  # 评论作者头像
    content = db.Column(db.Text, nullable=False)  # 评论内容
    date = db.Column(db.String(50), nullable=False)  # 评论时间

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "authorAvatar": self.authorAvatar,
            "content": self.content,
            "date": self.date
        }


# 帖子模型（后定义，因为依赖User）
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=False)  # 内容
    authorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键关联用户
    author = db.relationship('User', backref='posts')  # 关联User模型（反向查询）
    date = db.Column(db.String(50), nullable=False)  # 发布时间
    tags = db.Column(db.Text, nullable=False)  # 标签（逗号分隔）
    image = db.Column(db.String(100))  # 图片URL
    likes = db.Column(db.Integer, default=0)  # 点赞数
    type = db.Column(db.String(20), nullable=False)  # 分类（posts/questions/videos）
    comments = db.relationship('Comment', backref='post', lazy=True)  # 关联评论
    liked_users = db.relationship('User', secondary=post_likes, backref='liked_posts')  # 点赞用户

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": {
                "id": self.author.id,
                "username": self.author.username,
                "avatar": self.author.avatar
            },
            "authorId": self.authorId,
            "date": self.date,
            "tags": self.tags.split(',') if self.tags else [],
            "image": self.image,
            "likes": self.likes,
            "type": self.type,
            "comments": [c.to_dict() for c in self.comments],
            "isLiked": False,
        }


# 初始化数据库（关键：先删旧表，再建新表，确保结构正确）
with app.app_context():
    db.drop_all()
    db.create_all()

    # 测试用户1
    test_user1 = User(
        username="TechLover",
        email="tech@example.com",
        password="123456",
        avatar="/OIP-C.webp"
    )
    # 测试用户2
    test_user2 = User(
        username="GamerPro",
        email="game@example.com",
        password="123456",
        avatar="/OIP-C.webp"
    )
    db.session.add_all([test_user1, test_user2])
    db.session.commit()

    # 测试帖子1（posts类型）
    post1 = Post(
        title="如何选择合适的智能灯泡？",
        content="最近想入手智能灯泡，但品牌太多了，大家有什么推荐吗？主要关注亮度和连接稳定性...",
        authorId=test_user1.id,
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        tags="智能设备,灯泡,推荐",
        type="posts",
        likes=5
    )

    # 测试帖子2（questions类型）
    post2 = Post(
        title="Govee灯带连接不上WiFi怎么办？",
        content="刚买的Govee灯带，按照说明操作但一直连接不上WiFi，重启路由器也没用，有人遇到过吗？",
        authorId=test_user2.id,
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        tags="Govee,灯带,WiFi问题",
        type="questions",
        likes=12
    )
        # 测试帖子3（videos类型）
    post3 = Post(
        title="我的Govee灯光秀",
        content="分享一下用Govee产品做的家庭灯光秀，配合音乐效果很棒！",
        authorId=test_user1.id,
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        tags="Govee,灯光秀,照片",
        type="videos",
        image="1.png",
        likes=34
    )

    db.session.add_all([post1, post2,post3])
    db.session.commit()


# 接口：获取帖子列表
@app.route('/api/posts', methods=['GET'])
def get_posts():
    type_filter = request.args.get('type', 'all')
    posts = Post.query.all()
    if type_filter != 'all':
        posts = [p for p in posts if p.type == type_filter]  # 会正确筛选出type="videos"的帖子
    return jsonify([post.to_dict() for post in posts])

# 接口：获取帖子详情
@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


# 接口：注册
@app.route('/api/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "邮箱已注册"}), 400

    new_user = User(
        email=email,
        password=password,
        username=request.json.get('username', email.split('@')[0]),
        avatar=request.json.get('avatar', '/OIP-C.webp')
    )
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=email)
    return jsonify({
        "token": access_token,
        "user": new_user.to_dict()
    }), 201


# 接口：登录
@app.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        access_token = create_access_token(identity=email)
        return jsonify({
            "token": access_token,
            "user": user.to_dict()
        })
    return jsonify({"msg": "登录失败"}), 401


# 接口：点赞
@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def toggle_like(post_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    post = Post.query.get_or_404(post_id)

    if user in post.liked_users:
        post.liked_users.remove(user)
        post.likes -= 1
    else:
        post.liked_users.append(user)
        post.likes += 1

    db.session.commit()
    return jsonify({
        "likes": post.likes,
        "isLiked": user in post.liked_users
    })


# 接口：添加评论
@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    post = Post.query.get_or_404(post_id)

    new_comment = Comment(
        post_id=post_id,
        author=user.username,
        authorAvatar=user.avatar or '/OIP-C.webp',
        content=request.json.get('content'),
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(new_comment.to_dict()), 201


# 接口：创建帖子
@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "用户不存在"}), 404

    data = request.json
    new_post = Post(
        title=data.get('title'),
        content=data.get('content'),
        authorId=user.id,
        authorAvatar=user.avatar or '/avatars/default.jpg',
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        tags=data.get('tags'),
        type=data.get('type'),
        likes=0
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)