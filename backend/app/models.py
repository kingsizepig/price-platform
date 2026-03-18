from datetime import datetime
from app import db

class Category(db.Model):
    """商品分类"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, default=0)  # 父分类ID，0表示一级分类
    level = db.Column(db.Integer, default=1)  # 分类层级 1-3
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='approved')  # pending/approved/rejected
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Model):
    """商品信息"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(100))
    specs = db.Column(db.Text)  # JSON 规格参数
    images = db.Column(db.Text)  # JSON 图片URL数组
    origin_place = db.Column(db.String(100))  # 生产地
    shelf_life_days = db.Column(db.Integer)  # 保质期天数
    admin_price = db.Column(db.Numeric(12, 2))  # 管理员维护价格
    status = db.Column(db.String(20), default='pending')  # pending/approved/rejected
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creator_id = db.Column(db.Integer, nullable=False)  # 创建管理员ID

class User(db.Model):
    """用户"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    avatar = db.Column(db.String(255))
    integral = db.Column(db.Integer, default=0)  # 当前积分
    level = db.Column(db.Integer, default=1)  # L1-L5
    weight = db.Column(db.Numeric(3, 2), default=0.5)  # 价格权重
    status = db.Column(db.String(20), default='active')
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

class PriceRecord(db.Model):
    """用户录入价格记录"""
    __tablename__ = 'price_records'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(10), default='CNY')
    deal_date = db.Column(db.Date)  # 成交时间
    channel = db.Column(db.String(50), default='offline')  # 销售渠道
    location = db.Column(db.String(50))  # 所在地 省市
    quality = db.Column(db.String(20), default='new')  # 品相 new/90new/70new/used/expiring
    remaining_days = db.Column(db.Integer)  # 剩余保质期
    promotion = db.Column(db.String(100))  # 促销活动
    receipt_image = db.Column(db.String(255))  # 发票小票图片
    status = db.Column(db.String(20), default='active')  # active/deleted
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

class UserFavorite(db.Model):
    """用户自选商品"""
    __tablename__ = 'user_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_user_product'),
    )

class IntegralRecord(db.Model):
    """积分变动记录"""
    __tablename__ = 'integral_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    change = db.Column(db.Integer, nullable=False)  # 正数增加，负数减少
    reason = db.Column(db.String(100))  # 变动原因
    balance = db.Column(db.Integer, nullable=False)  # 变动后积分
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

class PriceCalibration(db.Model):
    """管理员标杆价格校准（用于用户权重评估）"""
    __tablename__ = 'price_calibrations'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    standard_price = db.Column(db.Numeric(12, 2), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
