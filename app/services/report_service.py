from app.extensions import db
from app.models.report import Report
from app.models.post import Post
from app.models.comment import Comment

class ReportService:
    @staticmethod
    def create_report(target_type, target_id, reporter_id, reason, created_at):
        # 验证目标存在性
        if target_type == 'post':
            target = Post.query.get(target_id)
        elif target_type == 'comment':
            target = Comment.query.get(target_id)
        else:
            return {"msg": "无效的举报类型"}, 400
            
        if not target:
            return {"msg": f"{target_type}不存在"}, 404
        
        try:
            new_report = Report(
                type=target_type,
                target_id=target_id,
                reporter_id=reporter_id,
                reason=reason,
                created_at=created_at
            )
            db.session.add(new_report)
            db.session.commit()
            return {"msg": "举报成功", "report": new_report.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": f"举报失败: {str(e)}"}, 500