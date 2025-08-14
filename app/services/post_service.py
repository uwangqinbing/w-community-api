from app.extensions import db
from app.models.post import Post
from app.models.user import User
from datetime import datetime

class PostService:
    @staticmethod
    def get_posts(type_filter='all'):
        posts = Post.query.all()
        if type_filter != 'all':
            posts = [p for p in posts if p.type == type_filter]
        return [post.to_dict() for post in posts]

    @staticmethod
    def get_post_detail(post_id):
        post = Post.query.get_or_404(post_id)
        return post.to_dict()

    @staticmethod
    def create_post(user, data):
        # user为当前登录用户对象
        new_post = Post(
            title=data.get('title'),
            content=data.get('content'),
            authorId=user.id,
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            tags=data.get('tags'),
            type=data.get('type'),
            image=data.get('image'),
            likes=0
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post.to_dict(), 201

    @staticmethod
    def toggle_like(user, post_id):
        post = Post.query.get_or_404(post_id)
        
        if user in post.liked_users:
            post.liked_users.remove(user)
            post.likes -= 1
        else:
            post.liked_users.append(user)
            post.likes += 1
        
        db.session.commit()
        return {
            "likes": post.likes,
            "isLiked": user in post.liked_users
        }