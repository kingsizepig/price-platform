"""
价格计算工具
- 管理员价格优先
- 加权平均算法 + 时间衰减 + 用户权重 + 异常值过滤
"""

import math
from datetime import datetime, timedelta
from collections import defaultdict

# 等级对应权重
LEVEL_WEIGHT = {
    1: 0.5,   # L1 新手
    2: 0.8,   # L2 初级
    3: 1.0,   # L3 中级 基准
    4: 1.2,   # L4 高级
    5: 1.5,   # L5 认证
}

# 时间衰减系数
def get_time_decay(created_time):
    """
    计算时间衰减系数
    7天内: 1.0
    8-30天: 0.8
    31-90天: 0.5
    91天+: 0.2
    """
    now = datetime.utcnow()
    delta = now - created_time
    days = delta.days
    
    if days <= 7:
        return 1.0
    elif days <= 30:
        return 0.8
    elif days <= 90:
        return 0.5
    else:
        return 0.2

def remove_outliers(prices):
    """移除偏离中位数 ±50% 的异常值"""
    if not prices:
        return []
    
    sorted_prices = sorted(prices)
    n = len(sorted_prices)
    mid = n // 2
    
    if n % 2 == 1:
        median = sorted_prices[mid]
    else:
        median = (sorted_prices[mid-1] + sorted_prices[mid]) / 2
    
    lower = median * 0.5
    upper = median * 1.5
    
    return [p for p in prices if lower <= p[0] <= upper]

def calculate_average_price(price_records, users):
    """
    计算加权平均价格
    price_records: [(price, user_level, create_time), ...]
    users: dict user_id -> level
    """
    # 过滤出90天内的数据
    now = datetime.utcnow()
    filtered = []
    
    for pr in price_records:
        days = (now - pr.create_time).days
        if days <= 90:
            level = users.get(pr.user_id, 1)
            filtered.append((float(pr.price), level, pr.create_time))
    
    if not filtered:
        return None
    
    # 移除异常值
    filtered_no_outliers = remove_outliers(filtered)
    if not filtered_no_outliers:
        filtered_no_outliers = filtered  #  fallback
    
    # 计算加权平均
    total_weighted = 0.0
    total_weight = 0.0
    
    for price, level, create_time in filtered_no_outliers:
        user_weight = LEVEL_WEIGHT.get(level, 0.5)
        time_decay = get_time_decay(create_time)
        weight = user_weight * time_decay
        
        total_weighted += price * weight
        total_weight += weight
    
    if total_weight == 0:
        return None
    
    return round(total_weighted / total_weight, 2)

def get_price_stats(price_records, users):
    """获取价格统计信息：最低、最高、中位数、加权平均"""
    if not price_records:
        return None
    
    # 过滤90天
    now = datetime.utcnow()
    prices = []
    for pr in price_records:
        if (now - pr.create_time).days <= 90:
            prices.append(float(pr.price))
    
    if not prices:
        return None
    
    prices_sorted = sorted(prices)
    n = len(prices_sorted)
    mid = n // 2
    
    if n % 2 == 1:
        median = prices_sorted[mid]
    else:
        median = (prices_sorted[mid-1] + prices_sorted[mid]) / 2
    
    weighted_avg = calculate_average_price(price_records, users)
    
    return {
        'min': min(prices),
        'max': max(prices),
        'median': round(median, 2),
        'weighted_avg': weighted_avg
    }

def group_by_location(price_records, users):
    """按地区分组计算平均价格"""
    result = defaultdict(list)
    for pr in price_records:
        if pr.location:
            result[pr.location].append((float(pr.price), users.get(pr.user_id, 1), pr.create_time))
    
    grouped_avg = {}
    for loc, items in result.items():
        if len(items) >= 3:  # 至少3条数据才有意义
            items_no_outliers = remove_outliers(items)
            if not items_no_outliers:
                items_no_outliers = items
            
            total_weighted = 0.0
            total_weight = 0.0
            for price, level, create_time in items_no_outliers:
                weight = LEVEL_WEIGHT.get(level, 0.5) * get_time_decay(create_time)
                total_weighted += price * weight
                total_weight += weight
            
            if total_weight > 0:
                grouped_avg[loc] = round(total_weighted / total_weight, 2)
    
    return grouped_avg

def group_by_channel(price_records, users):
    """按渠道分组计算平均价格"""
    result = defaultdict(list)
    for pr in price_records:
        channel = pr.channel or 'offline'
        result[channel].append((float(pr.price), users.get(pr.user_id, 1), pr.create_time))
    
    grouped_avg = {}
    for channel, items in result.items():
        if len(items) >= 2:
            items_no_outliers = remove_outliers(items)
            if not items_no_outliers:
                items_no_outliers = items
            
            total_weighted = 0.0
            total_weight = 0.0
            for price, level, create_time in items_no_outliers:
                weight = LEVEL_WEIGHT.get(level, 0.5) * get_time_decay(create_time)
                total_weighted += price * weight
                total_weight += weight
            
            if total_weight > 0:
                grouped_avg[channel] = round(total_weighted / total_weight, 2)
    
    return grouped_avg
