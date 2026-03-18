from flask import Blueprint, request, jsonify
from app import db
from app.models import Product, Category, PriceRecord, UserFavorite, User
from app.utils.price_calculator import calculate_average_price, get_price_stats, group_by_location, group_by_channel
from sqlalchemy import or_

bp = Blueprint('product', __name__)

@bp.route('/list', methods=['GET'])
def list_products():
    """商品列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    category_id = request.args.get('category_id', type=int)
    
    query = Product.query.filter_by(status='approved')
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    total = query.count()
    products = query.order_by(Product.update_time.desc()).offset((page-1)*page_size).limit(page_size).all()
    
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'name': p.name,
            'brand': p.brand,
            'origin_place': p.origin_place,
            'admin_price': float(p.admin_price) if p.admin_price else None,
        })
    
    return jsonify({
        'code': 0,
        'data': {
            'list': result,
            'total': total,
            'page': page,
            'page_size': page_size
        }
    })

@bp.route('/search', methods=['GET'])
def search():
    """搜索商品"""
    keyword = request.args.get('keyword', '').strip()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    if not keyword:
        return jsonify({'code': 400, 'message': '关键词不能为空'})
    
    query = Product.query.filter_by(status='approved').filter(
        or_(
            Product.name.contains(keyword),
            Product.brand.contains(keyword)
        )
    )
    
    total = query.count()
    products = query.order_by(Product.update_time.desc()).offset((page-1)*page_size).limit(page_size).all()
    
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'name': p.name,
            'brand': p.brand,
            'origin_place': p.origin_place,
        })
    
    return jsonify({
        'code': 0,
        'data': {
            'list': result,
            'total': total,
            'page': page
        }
    })

@bp.route('/detail/<int:product_id>', methods=['GET'])
def detail(product_id):
    """商品详情，包含价格计算"""
    product = Product.query.get(product_id)
    if not product or product.status != 'approved':
        return jsonify({'code': 404, 'message': '商品不存在'})
    
    # 获取所有激活价格
    price_records = PriceRecord.query.filter_by(
        product_id=product_id, 
        status='active'
    ).all()
    
    # 管理员价格优先
    current_price = None
    price_source = None
    if product.admin_price:
        current_price = float(product.admin_price)
        price_source = 'admin'
    
    stats = None
    location_prices = None
    channel_prices = None
    
    if price_records:
        # 获取用户等级映射
        user_ids = list(set(pr.user_id for pr in price_records))
        users = {u.id: u.level for u in User.query.filter(User.id.in_(user_ids)).all()}
        
        if not current_price:
            current_price = calculate_average_price(price_records, users)
            price_source = 'user_weighted'
        
        stats = get_price_stats(price_records, users)
        location_prices = group_by_location(price_records, users)
        channel_prices = group_by_channel(price_records, users)
    
    # 获取规格参数
    import json
    specs = {}
    if product.specs:
        try:
            specs = json.loads(product.specs)
        except:
            pass
    
    images = []
    if product.images:
        try:
            images = json.loads(product.images)
        except:
            pass
    
    return jsonify({
        'code': 0,
        'data': {
            'product': {
                'id': product.id,
                'name': product.name,
                'brand': product.brand,
                'category_id': product.category_id,
                'specs': specs,
                'images': images,
                'origin_place': product.origin_place,
                'shelf_life_days': product.shelf_life_days,
            },
            'price': {
                'current': current_price,
                'source': price_source,
                'stats': stats,
                'by_location': location_prices,
                'by_channel': channel_prices,
            }
        }
    })

@bp.route('/categories', methods=['GET'])
def get_categories():
    """获取分类树"""
    categories = Category.query.filter_by(status='approved').order_by(Category.sort).all()
    
    # 构建树形结构
    result = []
    parent_map = {}
    for c in categories:
        item = {
            'id': c.id,
            'name': c.name,
            'level': c.level,
            'children': []
        }
        if c.parent_id == 0:
            result.append(item)
        else:
            if c.parent_id not in parent_map:
                parent_map[c.parent_id] = []
            parent_map[c.parent_id].append(item)
    
    # 递归填充子节点
    def fill_children(parent_list):
        for p in parent_list:
            if p['id'] in parent_map:
                p['children'] = parent_map[p['id']]
                fill_children(p['children'])
    
    fill_children(result)
    
    return jsonify({'code': 0, 'data': result})

@bp.route('/favorite/add', methods=['POST'])
def add_favorite():
    """添加自选"""
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = request.headers.get('X-User-ID', type=int)  # 简化处理，实际用JWT
    
    if not user_id:
        return jsonify({'code': 401, 'message': '需要登录'})
    
    exists = UserFavorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    if exists:
        return jsonify({'code': 0, 'message': '已在自选列表中'})
    
    fav = UserFavorite(user_id=user_id, product_id=product_id)
    db.session.add(fav)
    db.session.commit()
    
    return jsonify({'code': 0, 'message': '添加成功'})

@bp.route('/favorite/remove', methods=['POST'])
def remove_favorite():
    """移除自选"""
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = request.headers.get('X-User-ID', type=int)
    
    fav = UserFavorite.query.filter_by(user_id=user_id, product_id=product_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
    
    return jsonify({'code': 0, 'message': '移除成功'})

@bp.route('/favorite/list', methods=['GET'])
def list_favorites():
    """用户自选列表"""
    user_id = request.headers.get('X-User-ID', type=int)
    if not user_id:
        return jsonify({'code': 401, 'message': '需要登录'})
    
    favs = UserFavorite.query.filter_by(user_id=user_id).all()
    product_ids = [f.product_id for f in favs]
    
    result = []
    for pid in product_ids:
        p = Product.query.get(pid)
        if p and p.status == 'approved':
            # 计算当前价格
            price_records = PriceRecord.query.filter_by(product_id=pid, status='active').all()
            current_price = None
            if p.admin_price:
                current_price = float(p.admin_price)
            elif price_records:
                user_ids = list(set(pr.user_id for pr in price_records))
                users = {u.id: u.level for u in User.query.filter(User.id.in_(user_ids)).all()}
                current_price = calculate_average_price(price_records, users)
            
            result.append({
                'id': p.id,
                'name': p.name,
                'brand': p.brand,
                'current_price': current_price,
            })
    
    return jsonify({'code': 0, 'data': result})
