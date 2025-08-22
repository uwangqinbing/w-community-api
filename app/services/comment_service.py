from app.extensions import db
from app.models.comment import Comment
from app.models.post import Post  # 新增导入，用于获取帖子信息

class CommentService:
    @staticmethod
    def delete_comment(username, post_id, comment_id, user_role, moderator_sections=None):
        """
        删除评论服务方法
        :param username: 当前登录用户名
        :param post_id: 帖子ID（用于验证评论所属关系）
        :param comment_id: 评论ID
        :param user_role: 用户角色（admin/moderator/user）
        :param moderator_sections: 版主管辖板块（仅版主需要）
        """
        # 1. 同时验证评论ID和所属帖子ID，确保数据一致性
        comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first()
        if not comment:
            return {"msg": "评论不存在或不属于该帖子"}, 404  # 更精确的错误信息
        
        try:
            # 2. 获取评论所属帖子（用于版主权限校验）
            post = Post.query.get(post_id)
            if not post:
                return {"msg": "评论所属的帖子不存在"}, 404

            # 3. 权限校验（支持多角色）
            has_permission = False
            
            # 3.1 管理员可删除所有评论
            if user_role == "admin":
                has_permission = True
            
            # 3.2 版主可删除管辖板块的评论（处理空格问题）
            elif user_role == "moderator":
                # 分割板块并去除空格，避免匹配失败
                sections = [s.strip() for s in (moderator_sections or "").split(',') if s.strip()]
                if post.section in sections:
                    has_permission = True
            
            # 3.3 普通用户只能删除自己的评论
            else:
                if comment.author == username:
                    has_permission = True

            if not has_permission:
                return {"msg": "没有删除权限"}, 403

            # 4. 执行删除操作
            db.session.delete(comment)
            db.session.commit()
            return {"msg": "评论删除成功"}, 200

        except Exception as e:
            db.session.rollback()
            # 记录具体错误但返回通用提示，避免泄露敏感信息
            print(f"删除评论异常: {str(e)}")
            return {"msg": "删除失败，请稍后重试"}, 500
    