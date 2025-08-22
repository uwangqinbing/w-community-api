from app.extensions import db

class Report(db.Model):
    __tablename__ = 'report'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'post' 或 'comment'
    target_id = db.Column(db.Integer, nullable=False)  # 帖子或评论ID
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "target_id": self.target_id,
            "reason": self.reason,
            "created_at": self.created_at
        }