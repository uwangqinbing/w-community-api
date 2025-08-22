from app.extensions import db
from app.models.comment import Comment

class CommentService:
    @staticmethod
    def delete_comment(username, post_id, comment_id):
        comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first()
        if not comment:
            return {"msg": "评论不存在"}, 404
        
        # 验证权限（只有评论作者可删除）
        if comment.author != username:
            return {"msg": "没有删除权限"}, 403
        
        try:
            db.session.delete(comment)
            db.session.commit()
            return {"msg": "评论删除成功"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"删除失败: {str(e)}"}, 500