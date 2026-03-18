from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.utils.integral import LEVEL_CONFIG

bp = Blueprint('user', __name__)

@bp.route('/info', methods=['GET'])
def info():
    """获取用户信息"""
    user_id = request.headers.get('X-User-ID', type=int)
    if not user_id:
        return jsonify({'code': 401, 'message': '需要登录'})
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'})
    
    # 获取等级名称
    level_name = next((c['name'] for c in LEVEL_CONFIG if c['level'] == user.level), 'L1 新手')
    
    return jsonify({
        'code': 0,
        'data': {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'integral': user.integral,
            'level': user.level,
            'level_name': level_name,
            'weight': float(user.weight) if user.weight else None,
        }
    })

@bp.route('/create', methods=['POST'])
def create():
    """创建用户（简化，实际需要注册流程）"""
    data = request.get_json()
    username = data.get('username')
    
    exists = User.query.filter_by(username=username).first()
    if exists:
        return jsonify({'code': 400, 'message': '用户名已存在'})
    
    user = User(
        username=username,
        integral=0,
        level=1,
        weight=0.5,
        status='active'
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': '创建成功',
        'data': {
            'id': user.id,
            'username': user.username,
            'integral': user.integral,
            'level': user.level
        }
    })

@bp.route('/levels', methods=['GET'])
def levels():
    """等级说明"""
    return jsonify({
        'code': 0,
        'data': LEVEL_CONFIG
    })
