"""
积分等级工具
"""

# 等级积分配置
LEVEL_CONFIG = [
    {'level': 1, 'name': 'L1 新手', 'min_points': 0, 'max_points': 99, 'weight': 0.5},
    {'level': 2, 'name': 'L2 初级', 'min_points': 100, 'max_points': 499, 'weight': 0.8},
    {'level': 3, 'name': 'L3 中级', 'min_points': 500, 'max_points': 1999, 'weight': 1.0},
    {'level': 4, 'name': 'L4 高级', 'min_points': 2000, 'max_points': 9999, 'weight': 1.2},
    {'level': 5, 'name': 'L5 认证', 'min_points': 10000, 'weight': 1.5},
]

def get_level_by_points(points):
    """根据积分计算等级"""
    for config in reversed(LEVEL_CONFIG):
        if points >= config['min_points']:
            return config['level'], config['weight']
    return 1, 0.5

def add_integral(db, user, change, reason):
    """
    添加积分，返回（是否成功，新积分，新等级）
    """
    user.integral += change
    new_points = user.integral
    new_level, new_weight = get_level_by_points(new_points)
    user.level = new_level
    user.weight = new_weight
    
    # 记录积分变动
    from app.models import IntegralRecord
    record = IntegralRecord(
        user_id=user.id,
        change=change,
        reason=reason,
        balance=new_points
    )
    db.session.add(record)
    db.session.commit()
    
    return True, new_points, new_level

def deduct_integral(db, user, change, reason):
    """
    扣除积分，返回（是否足够，新积分，新等级）
    """
    if user.integral < change:
        return False, user.integral, user.level
    
    user.integral -= change
    new_points = user.integral
    new_level, new_weight = get_level_by_points(new_points)
    user.level = new_level
    user.weight = new_weight
    
    from app.models import IntegralRecord
    record = IntegralRecord(
        user_id=user.id,
        change=-change,
        reason=reason,
        balance=new_points
    )
    db.session.add(record)
    db.session.commit()
    
    return True, new_points, new_level

def get_points_for_unlock(scope):
    """
    获取解锁所需积分
    scope: 'once' 单次 / 'monthly' 月订阅 / 'yearly' 年订阅
    """
    price_map = {
        'once': 5,
        'monthly': 20,
        'yearly': 200,
    }
    return price_map.get(scope, 5)
