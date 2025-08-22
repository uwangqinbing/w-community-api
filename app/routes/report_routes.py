from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.services.user_service import UserService
from app.services.report_service import ReportService

report_bp = Blueprint('report', __name__, url_prefix='/api')

@report_bp.route('/posts/<int:post_id>/report', methods=['POST'])
@jwt_required()
def report_post(post_id):
    return handle_report('post', post_id)

@report_bp.route('/comments/<int:comment_id>/report', methods=['POST'])
@jwt_required()
def report_comment(comment_id):
    return handle_report('comment', comment_id)

def handle_report(target_type, target_id):
    data = request.get_json()
    if not data or not data.get('reason'):
        return jsonify({"error": "举报原因不能为空"}), 400
    
    current_email = get_jwt_identity()
    user = UserService.get_user_by_email(current_email)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    result, status = ReportService.create_report(
        target_type=target_type,
        target_id=target_id,
        reporter_id=user.id,
        reason=data.get('reason'),
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    return jsonify(result), status