#!/usr/bin/env python3
from app import create_app, db
from app.models import Category

app = create_app()
with app.app_context():
    categories = [
        {'name': '房地产', 'parent_id': 0, 'level': 1, 'sort': 1, 'status': 'approved'},
        {'name': '金融资产', 'parent_id': 0, 'level': 1, 'sort': 2, 'status': 'approved'},
        {'name': '汽车', 'parent_id': 0, 'level': 1, 'sort': 3, 'status': 'approved'},
        {'name': '食品生鲜', 'parent_id': 0, 'level': 1, 'sort': 4, 'status': 'approved'},
        {'name': '日用品', 'parent_id': 0, 'level': 1, 'sort': 5, 'status': 'approved'},
        {'name': '奢侈品', 'parent_id': 0, 'level': 1, 'sort': 6, 'status': 'approved'},
        {'name': '医药健康', 'parent_id': 0, 'level': 1, 'sort': 7, 'status': 'approved'},
        {'name': '服务', 'parent_id': 0, 'level': 1, 'sort': 8, 'status': 'approved'},
    ]
    
    for cat in categories:
        exists = Category.query.filter_by(name=cat['name'], parent_id=cat['parent_id']).first()
        if not exists:
            c = Category(**cat)
            db.session.add(c)
    
    db.session.commit()
    print(f"✅ Inserted {len(categories)} root categories")
