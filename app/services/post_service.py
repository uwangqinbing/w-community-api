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

    # 只保留一个 get_post_detail 方法（删除重复定义）
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
            likes=0  # 假设模型字段是 likes
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post.to_dict(), 201
    
    @staticmethod
    def toggle_like(user_id, post_id):
        """基于 post.py 中的多对多关联表实现点赞（与模型匹配）"""
        post = Post.query.get(post_id)
        user = User.query.get(user_id)  # 获取用户对象（用于关联检查）
        
        if not post:
            return {"msg": "帖子不存在"}, 404
        if not user:
            return {"msg": "用户不存在"}, 404
        
        # 检查用户是否已点赞（使用 post.liked_users 关联）
        if user in post.liked_users:
            # 取消点赞：从多对多关联中移除
            post.liked_users.remove(user)
            post.likes = max(0, post.likes - 1)  # 避免负数
            db.session.commit()
            return {"msg": "取消点赞成功", "isLiked": False, "likes": post.likes}, 200
        else:
            # 新增点赞：添加到多对多关联
            post.liked_users.append(user)
            post.likes += 1
            db.session.commit()
            return {"msg": "点赞成功", "isLiked": True, "likes": post.likes}, 200
        
    @staticmethod
    def delete_post(user_id, post_id):
        post = Post.query.get(post_id)
        if not post:
           return {"msg": "帖子不存在"}, 404
    
        if post.authorId != user_id:
           return {"msg": "没有删除权限"}, 403
        try:
           db.session.delete(post)
           db.session.commit()
           return {"msg": "帖子删除成功"}, 200
        except Exception as e:
           db.session.rollback()
           return {"msg": f"删除失败: {str(e)}"}, 500