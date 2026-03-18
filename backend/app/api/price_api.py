from flask import Blueprint, request, jsonify
from app import db
from app.models import Product, PriceRecord, User, Product
from app.utils.integral import add_integral
from datetime import date

bp = Blueprint('price', __name__)

@bp.route('/create', methods=['POST'])
def create():
    """用户录入价格"""
    data = request.get_json()
    user_id = request.headers.get('X-User-ID', type=int)
    
    if not user_id:
        return jsonify({'code': 401, 'message': '需要登录'})
    
    product_id = data.get('product_id')
    price = data.get('price')
    
    if not product_id or not price:
        return jsonify({'code': 400, 'message': '商品ID和价格必填'})
    
    product = Product.query.get(product_id)
    if not product or product.status != 'approved':
        return jsonify({'code': 404, 'message': '商品不存在'})
    
    # 检查是否有这个商品的历史价格，判断是否是第一个价格
    has_existing = PriceRecord.query.filter_by(product_id=product_id).first() is not None
    
    # 创建价格记录
    pr = PriceRecord(
        product_id=product_id,
        user_id=user_id,
        price=price,
        currency=data.get('currency', 'CNY'),
        deal_date=data.get('deal_date', date.today().isoformat()),
        channel=data.get('channel', 'offline'),
        location=data.get('location'),
        quality=data.get('quality', 'new'),
        remaining_days=data.get('remaining_days'),
        promotion=data.get('promotion'),
    )
    db.session.add(pr)
    db.session.flush()
    
    # 给用户加积分
    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 401, 'message': '用户不存在'})
    
    if not has_existing:
        # 第一个价格，额外奖励
        add_integral(db, user, 20 + 5, f'首个录入商品 {product.name}')
    else:
        add_integral(db, user, 5, f'录入价格 {product.name}')
    
    db.session.commit()
    
    return jsonify({'code': 0, 'message': '录入成功', 'data': {'id': pr.id}})

@bp.route('/list/<int:product_id>', methods=['GET'])
def list_prices(product_id):
    """获取商品价格列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    query = PriceRecord.query.filter_by(product_id=product_id, status='active')
    total = query.count()
    records = query.order_by(PriceRecord.create_time.desc()).offset((page-1)*page_size).limit(page_size).all()
    
    result = []
    for pr in records:
        result.append({
            'id': pr.id,
            'price': float(pr.price),
            'deal_date': pr.deal_date.isoformat() if pr.deal_date else None,
            'channel': pr.channel,
            'location': pr.location,
            'quality': pr.quality,
            'create_time': pr.create_time.isoformat(),
        })
    
    return jsonify({
        'code': 0,
        'data': {
            'list': result,
            'total': total,
            'page': page
        }
    })

@bp.route('/user/my', methods=['GET'])
def my_records():
    """用户自己的录入历史"""
    user_id = request.headers.get('X-User-ID', type=int)
    if not user_id:
        return jsonify({'code': 401, 'message': '需要登录'})
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    query = PriceRecord.query.filter_by(user_id=user_id, status='active')
    total = query.count()
    records = query.order_by(PriceRecord.create_time.desc()).offset((page-1)*page_size).limit(page_size).all()
    
    result = []
    for pr in records:
        product = Product.query.get(pr.product_id)
        result.append({
            'id': pr.id,
            'product_id': pr.product_id,
            'product_name': product.name if product else None,
            'price': float(pr.price),
            'deal_date': pr.deal_date.isoformat() if pr.deal_date else None,
            'channel': pr.channel,
            'location': pr.location,
            'quality': pr.quality,
            'create_time': pr.create_time.isoformat(),
        })
    
    return jsonify({
        'code': 0,
        'data': {
            'list': result,
            'total': total,
            'page': page
        }
    })

@bp.route('/update/<int:price_id>', methods=['POST'])
def update(price_id):
    """用户修改自己录入的价格"""
    data = request.get_json()
    user_id = request.headers.get('X-User-ID', type=int)
    
    if not user_id:
        return jsonify({'code': 401, 'message': '需要登录'})
    
    pr = PriceRecord.query.get(price_id)
    if not pr or pr.user_id != user_id:
        return jsonify({'code': 404, 'message': '记录不存在'})
    
    if 'price' in data:
        pr.price = data['price']
    if 'deal_date' in data:
        pr.deal_date = data['deal_date']
    if 'channel' in data:
        pr.channel = data['channel']
    if 'location' in data:
        pr.location = data['location']
    if 'quality' in data:
        pr.quality = data['quality']
    if 'remaining_days' in data:
        pr.remaining_days = data['remaining_days']
    if 'promotion' in data:
        pr.promotion = data['promotion']
    
    db.session.commit()
    
    return jsonify({'code': 0, 'message': '修改成功'})

@bp.route('/delete/<int:price_id>', methods=['POST'])
def delete(price_id):
    """用户删除自己录入的价格"""
    user_id = request.headers.get('X-User-ID', type=int)
    
    if not user_id:
        return jsonify({'code': 401, 'message': '需要登录'})
    
    pr = PriceRecord.query.get(price_id)
    if not pr or pr.user_id != user_id:
        return jsonify({'code': 404, 'message': '记录不存在'})
    
    pr.status = 'deleted'
    db.session.commit()
    
    return jsonify({'code': 0, 'message': '删除成功'})
