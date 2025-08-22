from app.extensions import db

# 多对多关联表（帖子-点赞用户）
post_likes = db.Table(
    'post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    authorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='posts')  # 关联用户
    date = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(100))
    likes = db.Column(db.Integer, default=0)
    type = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(50), nullable=False, default='general')  # 板块名称
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")  # 级联删除评论
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